from flask import Blueprint, render_template, request, jsonify, current_app
from app.cipher.vigenere import VigenereCipher
from app.cipher.autokey_vigenere import AutoKeyVigenere
from app.cipher.extended_vigenere import ExtendedVigenere
from app.cipher.playfair import PlayfairCipher
from app.cipher.affine import AffineCipher

main = Blueprint('main', __name__)

# Cipher types configuration
CIPHER_TYPES = {
    'standard': VigenereCipher,
    'autokey': AutoKeyVigenere,
    'extended': ExtendedVigenere,
    'playfair': PlayfairCipher,
    'affine': AffineCipher
}

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/process', methods=['POST'])
def process():
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400

        # Extract fields with defaults
        text = data.get('text', '').strip()
        key = data.get('key', '').strip()
        operation = data.get('operation')
        cipher_type = data.get('cipher_type', 'standard').lower()

        # Debug logging
        print(f"Processing {operation} operation with {cipher_type} cipher")
        print(f"Input length: {len(text)}, Key length: {len(key)}")

        # Validate required fields
        if not all([text, key, operation]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: text, key, and operation are required'
            }), 400

        # Validate cipher type
        if cipher_type not in CIPHER_TYPES:
            return jsonify({
                'success': False,
                'error': f'Invalid cipher type. Must be one of: {", ".join(CIPHER_TYPES.keys())}'
            }), 400

        # Validate operation
        if operation not in ['encrypt', 'decrypt']:
            return jsonify({
                'success': False,
                'error': 'Invalid operation. Must be either encrypt or decrypt'
            }), 400

        # Get cipher instance
        cipher = CIPHER_TYPES[cipher_type]()
        
        # Process based on operation
        try:
            if operation == 'encrypt':
                result = cipher.encrypt(text, key)
            else:  # decrypt
                result = cipher.decrypt(text, key)
            
            print(f"Operation successful. Output length: {len(result)}")
            return jsonify({
                'success': True,
                'result': result
            })

        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            return jsonify({
                'success': False,
                'error': str(ve)
            }), 400

    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500