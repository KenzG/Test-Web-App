# playfair.py

class PlayfairCipher:
    def __init__(self):
        self.matrix_size = 5
        self.matrix = [['' for i in range(self.matrix_size)] for j in range(self.matrix_size)]

    def generate_key_matrix(self, key):
        # Menghapus spasi dan mengubah ke uppercase
        key = ''.join(key.upper().split())
        # Mengganti J dengan I
        key = key.replace('J', 'I')
        
        # Membuat set untuk karakter unik
        used_chars = set()
        matrix_vals = []
        
        # Menambahkan karakter dari key
        for char in key:
            if char.isalpha() and char not in used_chars:
                used_chars.add(char)
                matrix_vals.append(char)
        
        # Menambahkan sisa alphabet
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in used_chars:
                matrix_vals.append(char)
        
        # Membuat matrix
        k = 0
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                self.matrix[i][j] = matrix_vals[k]
                k += 1

    def find_position(self, char):
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if self.matrix[i][j] == char:
                    return i, j
        return -1, -1

    def prepare_text(self, text):
        # Menghapus karakter non-alphabet dan mengubah ke uppercase
        text = ''.join(c.upper() for c in text if c.isalpha())
        text = text.replace('J', 'I')
        
        # Menambahkan 'X' jika ada huruf yang berulang berpasangan
        result = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                result.append(text[i] + 'X')
                break
            if text[i] == text[i + 1]:
                result.append(text[i] + 'X')
                i += 1
            else:
                result.append(text[i] + text[i + 1])
                i += 2
                
        return result

    def encrypt(self, plaintext, key):
        try:
            self.generate_key_matrix(key)
            pairs = self.prepare_text(plaintext)
            result = []
            
            for pair in pairs:
                c1 = pair[0]
                c2 = pair[1]
                row1, col1 = self.find_position(c1)
                row2, col2 = self.find_position(c2)
                
                if row1 == row2:  # Same row
                    result.append(self.matrix[row1][(col1 + 1) % 5])
                    result.append(self.matrix[row2][(col2 + 1) % 5])
                elif col1 == col2:  # Same column
                    result.append(self.matrix[(row1 + 1) % 5][col1])
                    result.append(self.matrix[(row2 + 1) % 5][col2])
                else:  # Rectangle
                    result.append(self.matrix[row1][col2])
                    result.append(self.matrix[row2][col1])
            
            return ''.join(result)
        except Exception as e:
            raise ValueError(f"Playfair encryption failed: {str(e)}")

    def decrypt(self, ciphertext, key):
        try:
            self.generate_key_matrix(key)
            pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
            result = []
            
            for pair in pairs:
                c1 = pair[0]
                c2 = pair[1]
                row1, col1 = self.find_position(c1)
                row2, col2 = self.find_position(c2)
                
                if row1 == row2:  # Same row
                    result.append(self.matrix[row1][(col1 - 1) % 5])
                    result.append(self.matrix[row2][(col2 - 1) % 5])
                elif col1 == col2:  # Same column
                    result.append(self.matrix[(row1 - 1) % 5][col1])
                    result.append(self.matrix[(row2 - 1) % 5][col2])
                else:  # Rectangle
                    result.append(self.matrix[row1][col2])
                    result.append(self.matrix[row2][col1])
            
            return ''.join(result)
        except Exception as e:
            raise ValueError(f"Playfair decryption failed: {str(e)}")