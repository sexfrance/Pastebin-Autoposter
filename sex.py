import random
import hashlib
import hmac

class SuperSecureEncryption:
    def __init__(self, key):
        self.nums = '0123456789'
        self.chars = self.nums + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.rounds = 5  # Increased rounds
        # Generate multiple key derivatives
        self.master_key = self._derive_key(key)
        self.round_keys = self._generate_round_keys()
        self.sbox = self._create_sbox()

    def _derive_key(self, key):
        # Strong key derivation
        salt = b'static_salt_123'  # Could be made dynamic
        return hashlib.pbkdf2_hmac('sha512', 
                                  key.encode(), 
                                  salt,
                                  150000,  # High iteration count
                                  dklen=64)

    def _generate_round_keys(self):
        keys = []
        current = self.master_key
        for i in range(self.rounds):
            current = hmac.new(current, f"round{i}".encode(), 'sha256').digest()
            keys.append(current)
        return keys

    def _create_sbox(self):
        # Create substitution box using master key
        sbox = list(range(36))
        random.seed(int.from_bytes(self.master_key[:8], 'big'))
        random.shuffle(sbox)
        return sbox

    def _shuffle(self, chars, round_key, forward=True):
        state = list(range(len(chars)))
        # Use round key to generate permutation
        for i, byte in enumerate(round_key[:8]):
            j = byte % len(chars)
            state[i % len(chars)], state[j] = state[j], state[i % len(chars)]
        
        if forward:
            return ''.join(chars[i] for i in state)
        else:
            # Create inverse permutation
            inverse = [0] * len(state)
            for i, v in enumerate(state):
                inverse[v] = i
            return ''.join(chars[i] for i in inverse)

    def _transform_char(self, c, position, round_num, forward=True):
        idx = self.chars.index(c)
        key_byte = self.round_keys[round_num][position % 32]
        
        if forward:
            idx = (idx + key_byte) % 36
        else:
            idx = (idx - key_byte) % 36
        
        return self.chars[idx]

    def encrypt(self, text):
        if not all(c in self.chars for c in text.upper()):
            raise ValueError("Only 0-9 A-Z allowed")
        
        text = text.upper()
        result = text
        length_marker = self.chars[len(text) % 36]
        
        for round_num in range(self.rounds):
            # Transform
            temp = ''
            for pos, char in enumerate(result):
                temp += self._transform_char(char, pos, round_num, True)
            
            # Shuffle
            result = self._shuffle(list(temp), self.round_keys[round_num], True)
            
            # Simple substitution using round key
            result = ''.join(
                self.chars[(self.chars.index(c) + 
                          self.round_keys[round_num][i % 32]) % 36]
                for i, c in enumerate(result)
            )
        
        checksum = sum(self.chars.index(c) for c in result) % 36
        return length_marker + self.chars[checksum] + result

    def decrypt(self, text):
        if len(text) < 3:
            raise ValueError("Invalid ciphertext")
            
        length = self.chars.index(text[0])
        result = text[2:]
        
        for round_num in range(self.rounds - 1, -1, -1):
            # Reverse substitution
            result = ''.join(
                self.chars[(self.chars.index(c) - 
                          self.round_keys[round_num][i % 32]) % 36]
                for i, c in enumerate(result)
            )
            
            # Reverse shuffle
            result = self._shuffle(list(result), self.round_keys[round_num], False)
            
            # Reverse transform
            temp = ''
            for pos, char in enumerate(result):
                temp += self._transform_char(char, pos, round_num, False)
            result = temp
            
        return result[:length]

# Example
if __name__ == "__main__":
    enc = SuperSecureEncryption("ULTRAK3Y!")
    text = "HELLO123XYZ"
    encrypted = enc.encrypt(text)
    decrypted = enc.decrypt(encrypted)
    print(f"Original:  {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
