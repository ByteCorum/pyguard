from cryptography.fernet import Fernet
from zlib import compress, decompress
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305, Salsa20
from Crypto.Random import get_random_bytes
from os import urandom

class FernetCipher:
    @staticmethod
    def GenKey() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        fernet = Fernet(key)
        return fernet.encrypt(content)

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> str:
        fernet = Fernet(key)
        return fernet.decrypt(content).decode("utf-8")

class AesCipher:
    @staticmethod
    def GenKey(length=256) -> bytes:
        if length not in (128, 192, 256):
            raise Exception("AES-GCM: Bit length must be 128, 192, or 256")
        return urandom(length // 8)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        aes = AESGCM(key)
        nonce = urandom(12)
        return b64encode(nonce + aes.encrypt(nonce, content, associated_data=None))


    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> str:
        aes = AESGCM(key)

        content = b64decode(content)
        nonce = content[:12]
        ciphertext = content[12:]

        return aes.decrypt(
        nonce,
        ciphertext,
        associated_data=None
        ).decode("utf-8")

class ChaCha20Cipher:
    @staticmethod
    def GenKey() -> bytes:
        return get_random_bytes(32)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        cipher = ChaCha20.new(key=key)
        return b64encode(cipher.nonce + cipher.encrypt(content))

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> str:
        data = b64decode(content)
        nonce = data[:8]  # ChaCha20 nonce is 8 bytes
        ciphertext = data[8:]

        cipher = ChaCha20.new(key=key, nonce=nonce)
        return cipher.decrypt(ciphertext).decode("utf-8")

class Salsa20Cipher:
    @staticmethod
    def GenKey() -> bytes:
        return get_random_bytes(32)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        cipher = Salsa20.new(key=key)
        return b64encode(cipher.nonce + cipher.encrypt(content))

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> str:
        data = b64decode(content)
        nonce = data[:8]  # Salsa20 nonce is 8 bytes
        ciphertext = data[8:]

        cipher = Salsa20.new(key=key, nonce=nonce)
        return cipher.decrypt(ciphertext).decode("utf-8")