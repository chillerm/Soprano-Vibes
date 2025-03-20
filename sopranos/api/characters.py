from flask import Blueprint, jsonify, request
from ..models.character import characters, get_character_by_id, search_characters
from ..utils.errors import CharacterNotFoundError, InvalidInputError, handle_api_error
from ..utils.security import rate_limit, validate_input, add_security_headers

characters_bp = Blueprint('characters', __name__)

# Input validation schemas
search_schema = {
    'firstName': {'type': str, 'required': False},
    'lastName': {'type': str, 'required': False}
}

@characters_bp.route('/')
@rate_limit(limit=100, window=60)
@validate_input(search_schema)
def get_characters():
    """
    Get a list of all characters or search characters by first or last name.
    
    Query Parameters:
        firstName (str, optional): Filter characters by first name (case-insensitive partial match)
        lastName (str, optional): Filter characters by last name (case-insensitive partial match)
    
    Returns:
        JSON array of characters with status code 200
        Each character object contains:
            - id (int): Unique identifier
            - first_name (str): Character's first name
            - last_name (str): Character's last name
    
    Example:
        GET /api/characters/?firstName=Tony
        GET /api/characters/?lastName=Soprano
        GET /api/characters/?firstName=Tony&lastName=Soprano
    """
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    
    if first_name or last_name:
        response = jsonify([char.to_dict() for char in search_characters(first_name, last_name)])
    else:
        response = jsonify([char.to_dict() for char in characters])
    
    return add_security_headers(response)

@characters_bp.route('/<int:character_id>/')
@rate_limit(limit=100, window=60)
def get_character(character_id):
    """
    Get a specific character by ID.
    
    Args:
        character_id (int): The unique identifier of the character
    
    Returns:
        JSON object of the character with status code 200
        Character object contains:
            - id (int): Unique identifier
            - first_name (str): Character's first name
            - last_name (str): Character's last name
    
    Raises:
        404: If character is not found
    
    Example:
        GET /api/characters/1/
    """
    try:
        character = get_character_by_id(character_id)
        response = jsonify(character.to_dict())
        return add_security_headers(response)
    except CharacterNotFoundError as e:
        return handle_api_error(e)

# Register error handlers
@characters_bp.errorhandler(CharacterNotFoundError)
@characters_bp.errorhandler(InvalidInputError)
def handle_error(error):
    return handle_api_error(error) 