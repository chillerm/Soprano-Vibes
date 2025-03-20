from functools import wraps
from flask import request, current_app
from typing import Callable, Any
import re
from datetime import datetime, timedelta
from collections import defaultdict

# Rate limiting storage
request_counts = defaultdict(list)

def rate_limit(limit: int = 100, window: int = 60):
    """
    Rate limiting decorator.
    
    Args:
        limit (int): Maximum number of requests allowed
        window (int): Time window in seconds
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            ip = request.remote_addr
            now = datetime.now()
            
            # Clean old requests
            request_counts[ip] = [
                req_time for req_time in request_counts[ip]
                if now - req_time < timedelta(seconds=window)
            ]
            
            # Check rate limit
            if len(request_counts[ip]) >= limit:
                return current_app.response_class(
                    response='{"message": "Rate limit exceeded"}',
                    status=429,
                    mimetype='application/json'
                )
            
            # Add current request
            request_counts[ip].append(now)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def validate_input(schema: dict) -> Callable:
    """
    Input validation decorator.
    
    Args:
        schema (dict): Validation schema for request parameters
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.args.to_dict()
            
            for field, rules in schema.items():
                if field not in data:
                    if rules.get('required', False):
                        return current_app.response_class(
                            response=f'{{"message": "Missing required field: {field}"}}',
                            status=400,
                            mimetype='application/json'
                        )
                    continue
                
                value = data[field]
                
                # Type validation
                if 'type' in rules and not isinstance(value, rules['type']):
                    return current_app.response_class(
                        response=f'{{"message": "Invalid type for {field}"}}',
                        status=400,
                        mimetype='application/json'
                    )
                
                # Pattern validation
                if 'pattern' in rules and not re.match(rules['pattern'], str(value)):
                    return current_app.response_class(
                        response=f'{{"message": "Invalid format for {field}"}}',
                        status=400,
                        mimetype='application/json'
                    )
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def add_security_headers(response: Any) -> Any:
    """Add security headers to response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response 