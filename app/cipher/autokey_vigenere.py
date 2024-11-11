import base64

class AutoKeyVigenere:
    def __init__(self):
        print("AutoKeyVigenere instance created")

    def encrypt(self, plaintext, key):
        try:
            print(f"Encrypting with Auto-Key - Text: {plaintext}, Key: {key}")  # Debug log
            
            # Simpan case format
            case_map = ''.join('1' if c.isupper() else '0' for c in plaintext if c.isalpha())
            
            # Bersihkan input
            plaintext = ''.join(c.lower() for c in plaintext if c.isalpha())
            initial_key = ''.join(c.lower() for c in key if c.isalpha())
            
            if not plaintext or not initial_key:
                raise ValueError("Both text and key must contain valid characters")
            
            # Buat auto-key sesuai panjang plaintext
            auto_key = initial_key
            if len(auto_key) < len(plaintext):
                auto_key += plaintext[:len(plaintext) - len(initial_key)]
            
            print(f"Generated auto-key: {auto_key}")  # Debug log
            
            ciphertext = ""
            for i in range(len(plaintext)):
                p = ord(plaintext[i]) - ord('a')
                k = ord(auto_key[i]) - ord('a')
                c = (p + k) % 26
                ciphertext += chr(c + ord('a'))
            
            print(f"Ciphertext before encoding: {ciphertext}")  # Debug log
            
            # Simpan informasi untuk dekripsi
            final_text = f"{ciphertext}|{case_map}|{initial_key}"
            result = base64.b64encode(final_text.encode()).decode()
            
            print(f"Final encrypted result: {result}")  # Debug log
            return result
            
        except Exception as e:
            print(f"Autokey encryption error: {str(e)}")  # Debug log
            raise ValueError(f"Autokey encryption failed: {str(e)}")

    def decrypt(self, ciphertext, key):
        try:
            print(f"Decrypting Auto-Key - Ciphertext: {ciphertext}")  # Debug log
            
            # Decode base64
            decoded = base64.b64decode(ciphertext).decode()
            ciphertext, case_map, initial_key = decoded.split('|')
            
            print(f"Decoded parts - Ciphertext: {ciphertext}, Initial Key: {initial_key}")  # Debug log
            
            plaintext = ""
            # Inisialisasi current_key dengan initial_key
            current_key = initial_key.lower()
            
            for i in range(len(ciphertext)):
                # Perluas current_key jika diperlukan
                if i >= len(current_key):
                    current_key += plaintext[i - len(initial_key)].lower()
                
                c = ord(ciphertext[i]) - ord('a')
                k = ord(current_key[i]) - ord('a')
                p = (c - k + 26) % 26
                decrypted_char = chr(p + ord('a'))
    
                # Terapkan case mapping
                if i < len(case_map) and case_map[i] == '1':
                    decrypted_char = decrypted_char.upper()
                else:
                    decrypted_char = decrypted_char.lower()
                
                plaintext += decrypted_char
                
            print(f"Decrypted result: {plaintext}")  # Debug log
            return plaintext
            
        except Exception as e:
            print(f"Autokey decryption error: {str(e)}")  # Debug log
            raise ValueError(f"Autokey decryption failed: {str(e)}")
