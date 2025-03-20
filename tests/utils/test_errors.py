import pytest
from flask import Flask, jsonify
from sopranos.utils.errors import (
    APIError,
    CharacterNotFoundError,
    InvalidInputError,
    handle_api_error
)

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_api_error():
    error = APIError("Test error", status_code=400)
    assert error.message == "Test error"
    assert error.status_code == 400
    assert error.payload == {}
    
    data = error.to_dict()
    assert data['message'] == "Test error"
    assert data['status_code'] == 400

def test_character_not_found_error():
    error = CharacterNotFoundError(123)
    assert error.message == "Character with ID 123 not found"
    assert error.status_code == 404

def test_invalid_input_error():
    error = InvalidInputError("Invalid input")
    assert error.message == "Invalid input"
    assert error.status_code == 400

def test_handle_api_error(app):
    with app.app_context():
        error = APIError("Test error", status_code=400)
        response = handle_api_error(error)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['message'] == "Test error"
        assert data['status_code'] == 400

def test_error_with_payload():
    payload = {'field': 'value'}
    error = APIError("Test error", status_code=400, payload=payload)
    data = error.to_dict()
    
    assert data['message'] == "Test error"
    assert data['status_code'] == 400
    assert data['field'] == 'value' 