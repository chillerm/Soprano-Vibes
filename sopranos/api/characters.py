from flask import Blueprint, jsonify
from ..models.character import characters

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/')
def get_characters():
    return jsonify([character.to_dict() for character in characters]) 