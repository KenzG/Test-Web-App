# affine.py

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

class AffineCipher:
    def __init__(self):
        self.ALPHABET_SIZE = 26
        # Daftar nilai a yang valid (coprime dengan 26)
        self.VALID_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    def validate_keys(self, a, b):
        if a not in self.VALID_A:
            raise ValueError(f"Invalid 'a' value. Must be one of: {self.VALID_A}")
        if not 0 <= b < self.ALPHABET_SIZE:
            raise ValueError(f"Invalid 'b' value. Must be between 0 and {self.ALPHABET_SIZE-1}")

    def process_text(self, text):
        return ''.join(c.upper() for c in text if c.isalpha())

    def encrypt(self, plaintext, key):
        try:
            # Parse key format "a,b"
            try:
                a, b = map(int, key.split(','))
            except:
                raise ValueError("Key must be in format 'a,b' (e.g., '5,8')")
            
            self.validate_keys(a, b)
            plaintext = self.process_text(plaintext)
            result = []
            
            for char in plaintext:
                if char.isalpha():
                    # Convert to 0-25 range
                    x = ord(char) - ord('A')
                    # Apply affine transformation
                    encrypted = (a * x + b) % self.ALPHABET_SIZE
                    # Convert back to character
                    result.append(chr(encrypted + ord('A')))
                else:
                    result.append(char)
            
            return ''.join(result)
        except Exception as e:
            raise ValueError(f"Affine encryption failed: {str(e)}")

    def decrypt(self, ciphertext, key):
        try:
            # Parse key format "a,b"
            try:
                a, b = map(int, key.split(','))
            except:
                raise ValueError("Key must be in format 'a,b' (e.g., '5,8')")
            
            self.validate_keys(a, b)
            ciphertext = self.process_text(ciphertext)
            result = []
            
            # Calculate modular multiplicative inverse of a
            a_inv = modinv(a, self.ALPHABET_SIZE)
            
            for char in ciphertext:
                if char.isalpha():
                    # Convert to 0-25 range
                    y = ord(char) - ord('A')
                    # Apply affine decryption
                    decrypted = (a_inv * (y - b)) % self.ALPHABET_SIZE
                    # Convert back to character
                    result.append(chr(decrypted + ord('A')))
                else:
                    result.append(char)
            
            return ''.join(result)
        except Exception as e:
            raise ValueError(f"Affine decryption failed: {str(e)}")