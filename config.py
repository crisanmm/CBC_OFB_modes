from Crypto.Cipher import AES

initialization_vector = b'\x16\x40\x1f\x3e\x44\xa0\x81\x09\x2d\x3b\x52\x78\x57\x9c\xe4\x26'
K_prime = b'\xdc\xf8\x80\x88\x4f\xa2\x05\x98\x4a\x3c\xd6\xe2\xf6\xe3\x69\x04'

cipher = AES.new(key=K_prime, mode=AES.MODE_ECB)
cipher.block_size = AES.block_size


class CBC:
    """Convenience class for the CBC mode of operation

    Provides encrypting and decrypting functionality.
    """

    def __init__(self, iv, key):
        self.iv = iv
        self.key = key

    def encrypt_block(self, plaintext):
        plaintext_xor_iv = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(plaintext, self.iv))
        cipher_block = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(plaintext_xor_iv, self.key))
        self.iv = cipher_block
        return cipher_block

    def decrypt_block(self, ciphertext):
        ciphertext_xor_key = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(ciphertext, self.key))
        plain_block = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(ciphertext_xor_key, self.iv))
        self.iv = ciphertext
        return plain_block


class OFB:
    """Convenience class for the OFB mode of operation

    Provides encrypting and decrypting functionality.
    """

    def __init__(self, iv, key):
        self.iv = iv
        self.key = key

    def encrypt_block(self, plaintext):
        iv_xor_key = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(self.iv, self.key))
        cipher_block = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(iv_xor_key, plaintext))
        self.iv = cipher_block
        return cipher_block

    def decrypt_block(self, ciphertext):
        iv_xor_key = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(self.iv, self.key))
        plain_block = bytes(byte1 ^ byte2 for (byte1, byte2) in zip(iv_xor_key, ciphertext))
        self.iv = ciphertext
        return plain_block
