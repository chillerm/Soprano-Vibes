from flask import Flask
from .api import characters_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(characters_bp, url_prefix='/api/characters')
    
    return app 