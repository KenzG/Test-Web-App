import base64

class ExtendedVigenere:
    def __init__(self):
        print("ExtendedVigenere instance created")

    def encrypt(self, plaintext, key):
        try:
            if not plaintext or not key:
                raise ValueError("Both text and key must not be empty")
            
            # Convert plaintext and key to bytes directly
            plaintext_bytes = plaintext.encode('utf-8')
            key_bytes = key.encode('utf-8')
            key_length = len(key_bytes)
            
            ciphertext_bytes = bytearray()
            
            # Perform byte-by-byte encryption
            for i in range(len(plaintext_bytes)):
                p = plaintext_bytes[i]
                k = key_bytes[i % key_length]
                c = (p + k) % 256
                ciphertext_bytes.append(c)
            
            # Convert to base64 for safe transmission
            return base64.b64encode(ciphertext_bytes).decode('ascii')
            
        except Exception as e:
            print(f"Extended encryption error: {str(e)}")
            raise ValueError(f"Extended encryption failed: {str(e)}")

    def decrypt(self, ciphertext, key):
        try:
            if not ciphertext or not key:
                raise ValueError("Both text and key must not be empty")

            # First decode the base64 ciphertext
            try:
                ciphertext_bytes = base64.b64decode(ciphertext)
            except Exception as e:
                raise ValueError("Invalid base64 input")
            
            key_bytes = key.encode('utf-8')
            key_length = len(key_bytes)
            
            plaintext_bytes = bytearray()
            
            # Perform byte-by-byte decryption
            for i in range(len(ciphertext_bytes)):
                c = ciphertext_bytes[i]
                k = key_bytes[i % key_length]
                p = (c - k) % 256
                plaintext_bytes.append(p)
            
            # Try to decode the resulting bytes to UTF-8
            try:
                return plaintext_bytes.decode('utf-8')
            except UnicodeDecodeError as e:
                raise ValueError("Decryption resulted in invalid UTF-8 sequence. " + 
                               "Please check if the key and ciphertext are correct.")
            
        except Exception as e:
            print(f"Extended decryption error: {str(e)}")
            raise ValueError(f"Extended decryption failed: {str(e)}")