import string

class EncryptionUtils:
    def __init__(self, key: str):
        self.key = key

    def caesar_cipher(self, plaintext: str, shift: int) -> str:
        ciphertext = ''
        for ch in plaintext:
            if ch.isalpha():
                ascii_offset = 65 if ch.isupper() else 97
                shifted = ((ord(ch.lower()) - ord('a') + shift) % 26) + ascii_offset
                ciphertext += chr(shifted)
            else:
                ciphertext += ch
        return ciphertext

    def vigenere_cipher(self, plain_text: str) -> str:
        encrypted_text = ''
        key_index = 0
        key_len = len(self.key)
        for ch in plain_text:
            if ch.isalpha():
                shift = ord(self.key[key_index % key_len].lower()) - ord('a')
                base = ord('a')
                encrypted_char = chr(((ord(ch.lower()) - base + shift) % 26) + base)
                encrypted_text += encrypted_char.upper() if ch.isupper() else encrypted_char
                key_index += 1
            else:
                encrypted_text += ch
        return encrypted_text

    def rail_fence_cipher(self, plain_text: str, rails: int) -> str:
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        fence = ['' for _ in range(rails)]
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row] += ch
            row += direction

        encrypted_text = ''.join(fence)
        return encrypted_text
