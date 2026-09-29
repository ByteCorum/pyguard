from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESGCMSIV
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

class FernetMethod:
    @staticmethod
    def GenKey() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        fernet = Fernet(key)
        return fernet.encrypt(content)

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> bytes:
        fernet = Fernet(key)
        return fernet.decrypt(content)

class AesGcmMethod: # Present but unused in releases cuz covered by XChaCha20Poly1305Method
    @staticmethod
    def GenKey(length: int = 256) -> bytes:
        if length not in (128, 192, 256):
            raise ValueError("AES-GCM: Bit length must be 128, 192, or 256")

        return get_random_bytes(length // 8)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        aes = AESGCM(key)
        nonce: bytes = get_random_bytes(12)
        return b64encode(nonce + aes.encrypt(nonce, content, associated_data=None))

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> bytes:
        aes = AESGCM(key)
        content = b64decode(content)
        if len(content) < 12:
            raise ValueError("AES-GCM: Ciphertext too short")

        nonce: bytes = content[:12]
        ciphertext: bytes = content[12:]

        return aes.decrypt(
            nonce,
            ciphertext,
            associated_data=None
        )

class AesGcmSivMethod:
    @staticmethod
    def GenKey(length: int = 256) -> bytes:
        if length not in (128, 192, 256):
            raise ValueError("AES-GCM-SIV: Bit length must be 128, 192, or 256")
        return get_random_bytes(length // 8)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        aes = AESGCMSIV(key)
        nonce: bytes = get_random_bytes(12)
        return b64encode(nonce + aes.encrypt(nonce, content, associated_data=None))

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> bytes:
        aes = AESGCMSIV(key)
        content = b64decode(content)
        if len(content) < 12:
            raise ValueError("AES-GCM-SIV: Ciphertext too short")

        nonce: bytes = content[:12]
        ciphertext: bytes = content[12:]

        return aes.decrypt(
            nonce,
            ciphertext,
            associated_data=None
        )

class ChaCha20Poly1305Method: # Present but unused in releases cuz covered by XChaCha20Poly1305Method
    @staticmethod
    def GenKey() -> bytes:
        return get_random_bytes(32)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        nonce: bytes = get_random_bytes(12)
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        ciphertext: bytes = cipher.encrypt(content)
        mac: bytes = cipher.digest()
        return b64encode(nonce + ciphertext + mac)

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> bytes:
        data: bytes = b64decode(content)

        if len(data) < 12 + 16:
            raise ValueError("ChaCha20-Poly1305: Ciphertext too short")

        nonce: bytes = data[:12]
        # The 16-byte Poly1305 tag is stored at the end of the payload.
        mac: bytes = data[-16:]
        # Ciphertext lies between the 12-byte nonce and the 16-byte tag.
        ciphertext: bytes = data[12:-16]

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, mac)

class XChaCha20Poly1305Method:
    @staticmethod
    def GenKey() -> bytes:
        return get_random_bytes(32)

    @staticmethod
    def Encrypt(key: bytes, content: bytes) -> bytes:
        nonce: bytes = get_random_bytes(24)
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        ciphertext: bytes = cipher.encrypt(content)
        mac: bytes = cipher.digest()
        return b64encode(nonce + ciphertext + mac)

    @staticmethod
    def Decrypt(key: bytes, content: bytes) -> bytes:
        data: bytes = b64decode(content)

        if len(data) < 24 + 16:
            raise ValueError("XChaCha20-Poly1305: Ciphertext too short")

        # XChaCha20 uses a 24-byte extended nonce.
        nonce: bytes = data[:24]
        # The 16-byte Poly1305 tag is stored at the end of the payload.
        mac: bytes = data[-16:]
        # Ciphertext lies between the 24-byte nonce and the 16-byte tag.
        ciphertext: bytes = data[24:-16]
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, mac)
