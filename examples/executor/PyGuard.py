from hashlib import sha256
from os import path, getcwd
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import Salsa20
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet

from base64 import b64decode, b64encode
from zlib import decompress
from sys import exit

_ = exec

class PyGuard:
    def __init__(self, code, file):
        try:
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = code
            self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = file
            code = None
            file = None

            self.__CheckHashe812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__Decrypte812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)

    def __dir__(self) -> list[str]:
        return []

    def __CheckHashe812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        try:
            self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = path.relpath(self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196, getcwd())

            with open(self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196, 'rb') as file:
                fileHash = sha256(file.read()).hexdigest()

            for file in [['test.py', 'dbfe6141f98e4332a375ad88ee1cd27a493d7889f1099420f6c3f3a140c38531']]:
                if path.samefile(self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196, file[0]) and fileHash == file[1]:
                    self.__filee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = None
                    return

            raise Exception("Invalid file hash")
        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)

    def __Decrypte812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        try:
            self.__Base64e812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[::-1]
            self.__Recursivee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__Salsae812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__ChaChae812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__Aese812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__Fernete812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__Base64e812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()

            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[::-1]
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196.decode('utf-8')

            self.__ReturnVariablese812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196()
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64encode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196.encode('utf-8'))

        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)

    @property
    def _(self):
        return compile(b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196).decode('utf-8'), '<string>', 'exec')

    def __Recursivee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        for i in range(4):
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[::-1]
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)

    def __Salsae812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        nonce = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[:8]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[8:]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = Salsa20.new(key=b'\x89\xf9\xfe\xa7\xa3\x9eH\xc4}\t\x17\xe2\xcc\xf4\x04\xc0D\xb8^\xa2\x83\x98t\x02\x1a\xc7X\xc7^x\x8cD', nonce=nonce).decrypt(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)

    def __ChaChae812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        nonce = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[:8]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[8:]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = ChaCha20.new(key=b'\xcb\x80\xbc\xbc\xe6/\xec/cW\xfb\xb4\xdc\xea\x10\x89T\xf4\x1b\xe8n\xf3Yo<(u\x8b\x0b\x0f\xb9\x01', nonce=nonce).decrypt(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)

    def __Aese812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        aes = AESGCM(b'I\xd2g\x16\xf2Q\xc8\x18{G\xfc\x92\x9bJ\xa4\xf6\xaa\x86\x93\x9e\x057\xed\xfcW\xb0\xc1h2g>o')
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        nonce = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[:12]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196[12:]
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = aes.decrypt(nonce, self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196, associated_data=None)

    def __Fernete812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        fernet = Fernet(b'n0CpWIEXgW1w1ndHL5DTd9lqNEHJghbQTUqeOFNmKeE=')
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = fernet.decrypt(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)

    def __Base64e812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = decompress(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)
        self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = b64decode(self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196)

    def __ReturnVariablese812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196(self):
        for raw in [['758fdfe317470e2ceb8e04c64de9d95470bf28a64f23af3439f3c7d181300df1', b'x\x9c\x0b\xa8\xd4\r\xce\xc8L\xcdI\x01\x00\x0f\xe5\x03P']]:
            string = decompress(raw[1]).decode("utf-8")
            self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196 = self.__codee812520fd9c71232668515d6bd91bd4c386f014e41cc3bdd9262101759019196.replace(raw[0], string)
