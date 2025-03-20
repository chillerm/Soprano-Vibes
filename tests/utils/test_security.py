import pytest
from flask import Flask, request, jsonify
from sopranos.utils.security import rate_limit, validate_input, add_security_headers
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_rate_limit(app):
    with app.app_context():
        @app.route('/test/')
        @rate_limit(limit=2, window=1)  # Short window for testing
        def test_endpoint():
            return jsonify({'message': 'success'})
        
        client = app.test_client()
        
        # Reset rate limit for this test
        from sopranos.utils.security import request_counts
        request_counts.clear()
        
        # First request should succeed
        response = client.get('/test/')
        assert response.status_code == 200
        
        # Second request should succeed
        response = client.get('/test/')
        assert response.status_code == 200
        
        # Third request should be rate limited
        response = client.get('/test/')
        assert response.status_code == 429
        data = response.get_json()
        assert data['message'] == 'Rate limit exceeded'

def test_validate_input(app):
    with app.app_context():
        schema = {
            'name': {'type': str, 'required': True},
            'age': {'type': str, 'required': False}  # Query params are always strings
        }
        
        @app.route('/test/')
        @validate_input(schema)
        def test_endpoint():
            return jsonify({'message': 'success'})
        
        client = app.test_client()
        
        # Missing required field
        response = client.get('/test/')
        assert response.status_code == 400
        data = response.get_json()
        assert 'Missing required field' in data['message']
        
        # Valid input
        response = client.get('/test/?name=John&age=30')
        assert response.status_code == 200

def test_security_headers(app):
    @app.route('/test/')
    def test_endpoint():
        response = jsonify({'message': 'success'})
        return add_security_headers(response)
    
    client = app.test_client()
    response = client.get('/test/')
    
    # Check security headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'
    assert response.headers['X-XSS-Protection'] == '1; mode=block'
    assert 'Strict-Transport-Security' in response.headers 