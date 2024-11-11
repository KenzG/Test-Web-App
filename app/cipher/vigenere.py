# app/cipher/vigenere.py

import base64

class VigenereCipher:
    def __init__(self):
        print("VigenereCipher instance created")  # Debug log

    def encrypt(self, plaintext, key):
        try:
            print(f"Encrypting text: {plaintext} with key: {key}")  # Debug log
            
            # Simpan case format dalam bentuk bit string
            case_map = ''.join('1' if c.isupper() else '0' for c in plaintext if c.isalpha())
            
            # Clean input
            plaintext = ''.join(c.lower() for c in plaintext if c.isalpha())
            key = ''.join(c.lower() for c in key if c.isalpha())
            
            if not plaintext or not key:
                raise ValueError("Both text and key must contain valid characters")
            
            ciphertext = ""
            key_length = len(key)
            
            for i in range(len(plaintext)):
                p = ord(plaintext[i]) - ord('a')
                k = ord(key[i % key_length]) - ord('a')
                c = (p + k) % 26
                ciphertext += chr(c + ord('a'))
            
            # Gabungkan ciphertext dengan case map dalam format yang lebih ringkas
            final_text = f"{ciphertext}|{case_map}"
            result = base64.b64encode(final_text.encode()).decode()
            print(f"Encryption result: {result}")  # Debug log
            return result
            
        except Exception as e:
            print(f"Encryption error: {str(e)}")  # Debug log
            raise ValueError(f"Encryption failed: {str(e)}")

    def decrypt(self, ciphertext, key):
        try:
            print(f"Decrypting text: {ciphertext} with key: {key}")  # Debug log
            
            # Decode base64 dan pisahkan ciphertext dan case map
            decoded = base64.b64decode(ciphertext).decode()
            ciphertext, case_map = decoded.split('|')
            
            key = ''.join(c.lower() for c in key if c.isalpha())
            
            if not ciphertext or not key:
                raise ValueError("Both text and key must contain valid characters")
            
            plaintext = ""
            key_length = len(key)
            
            for i in range(len(ciphertext)):
                c = ord(ciphertext[i]) - ord('a')
                k = ord(key[i % key_length]) - ord('a')
                p = (c - k) % 26
                # Terapkan case sesuai mapping
                char = chr(p + ord('a'))
                if i < len(case_map) and case_map[i] == '1':
                    char = char.upper()
                plaintext += char
            
            print(f"Decryption result: {plaintext}")  # Debug log
            return plaintext
            
        except Exception as e:
            print(f"Decryption error: {str(e)}")  # Debug log
            raise ValueError(f"Decryption failed: {str(e)}")