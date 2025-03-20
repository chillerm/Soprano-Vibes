from flask import Blueprint, jsonify, request, abort
from ..models.character import characters, get_character_by_id, search_characters

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/')
def get_characters():
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    
    if first_name or last_name:
        return jsonify([char.to_dict() for char in search_characters(first_name, last_name)])
    return jsonify([char.to_dict() for char in characters])

@characters_bp.route('/<int:character_id>')
def get_character(character_id):
    character = get_character_by_id(character_id)
    if character is None:
        abort(404)
    return jsonify(character.to_dict()) 