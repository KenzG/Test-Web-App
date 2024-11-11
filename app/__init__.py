from flask import Flask
from flask_cors import CORS
from config import Config
from app.cipher.vigenere import VigenereCipher
from app.cipher.autokey_vigenere import AutoKeyVigenere
from app.cipher.extended_vigenere import ExtendedVigenere

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize cipher instances
    app.cipher_instances = {
        'standard': VigenereCipher(),
        'autokey': AutoKeyVigenere(),
        'extended': ExtendedVigenere()
    }
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app