from flask import Flask
from .api.characters import characters_bp
from .utils.errors import APIError, CharacterNotFoundError, InvalidInputError, handle_api_error

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(characters_bp, url_prefix='/api/characters')
    
    # Register error handlers
    app.register_error_handler(APIError, handle_api_error)
    app.register_error_handler(CharacterNotFoundError, handle_api_error)
    app.register_error_handler(InvalidInputError, handle_api_error)
    
    return app 