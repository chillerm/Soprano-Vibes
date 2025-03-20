from typing import Any, Dict, Optional
from flask import jsonify
from werkzeug.exceptions import HTTPException

class APIError(HTTPException):
    """Base class for all API errors."""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None
    ):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        rv = dict(self.payload)
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

    def __str__(self) -> str:
        return self.message

class CharacterNotFoundError(APIError):
    """Raised when a character is not found."""
    def __init__(self, character_id: int):
        message = f"Character with ID {character_id} not found"
        super().__init__(
            message=message,
            status_code=404
        )

class InvalidInputError(APIError):
    """Raised when input validation fails."""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=400
        )

def handle_api_error(error: APIError):
    """Handle API errors and return JSON response."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response 