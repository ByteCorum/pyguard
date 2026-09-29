from config import NAME, VERSION
from utils.crypto import FernetMethod, b64encode
from zlib import compress
from random import choice
from string import ascii_letters, digits

class LegacyObfuscation:
    def __init__(self, mode: int, loops: int, separator: str) -> None:
        if mode < 1 or mode > 4:
            raise Exception("Invalid mode value")
        if loops < 1:
            raise Exception("Invalid loops value")

        self.mode = mode
        self.loops = loops
        self.separator = separator

    def Encrypt(self, content: str) -> str:
        for i in range(self.loops):
            match self.mode:
                case 1:
                    content = self.LiteObfuscation(content)
                case 2:
                    content = self.NormalObfuscation(content)
                case 3:
                    content = self.MediumObfuscation(content)
                case 4:
                    content = self.PowerObfuscateion(content)
                case _:
                    raise Exception("Invalid mode value")

        return content

    def Wrap(self, content: str) -> str:
        match self.mode:
            case 1:
                return f"#Obfuscated by {NAME}\n_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode((__import__('zlib').decompress(__))[::-1])[::-1]);"+content
            case 2:
                return f"#Obfuscated by {NAME}\n_=lambda __:__import__('zlib').decompress(__import__('cryptography.fernet').fernet.Fernet(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1]).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])[::-1]);"+content
            case 3:
                return f"#Obfuscated by {NAME}\n_=lambda __:__import__('zlib').decompress(__import__('cryptography.fernet').fernet.Fernet(__import__('base64').b64decode(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1])).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])[::-1]);"+content
            case 4:
                return f"#Obfuscated by {NAME}\n_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode(__import__('zlib').decompress((__import__('cryptography.fernet').fernet.Fernet(__import__('base64').b64decode(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1])).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])))[::-1]));"+content
            case _:
                raise Exception("Invalid mode value")

    def PowerObfuscateion(self, content: str) -> str:
        bytestr:bytes = content.encode('utf-8')

        bytestr = compress(bytestr)
        bytestr = b64encode(bytestr)
        bytestr = bytestr[::-1]
        bytestr = compress(bytestr)

        key:bytes = FernetMethod.GenKey()
        # TODO encode separator with b64encode
        bytestr = FernetMethod.Encrypt(key,bytestr)+self.separator.encode("utf-8")+b64encode(key)

        bytestr = bytestr[::-1]
        bytestr = compress(bytestr)

        return f"exec((_)({bytestr}))"

    def MediumObfuscation(self, content: str) -> str:
        bytestr:bytes = content.encode('utf-8')

        bytestr = compress(bytestr)
        bytestr = bytestr[::-1]

        key:bytes = FernetMethod.GenKey()
        # TODO encode separator with b64encode
        bytestr = FernetMethod.Encrypt(key, bytestr)+self.separator.encode("utf-8")+b64encode(key)

        bytestr = bytestr[::-1]
        bytestr = compress(bytestr)

        return f"exec((_)({bytestr}))"

    def NormalObfuscation(self, content: str) -> str:
        bytestr:bytes = content.encode('utf-8')

        bytestr = compress(bytestr)
        bytestr = bytestr[::-1]

        key:bytes = FernetMethod.GenKey()
        bytestr = FernetMethod.Encrypt(key, bytestr) + self.separator.encode("utf-8") + key

        bytestr = bytestr[::-1]
        bytestr = compress(bytestr)

        return f"exec((_)({bytestr}))"

    def LiteObfuscation(self, content:str) -> str:
        bytestr:bytes = content.encode('utf-8')

        bytestr = compress(bytestr)
        bytestr = bytestr[::-1]

        bytestr = b64encode(bytestr)

        bytestr = bytestr[::-1]
        bytestr = compress(bytestr)

        return f"exec((_)({bytestr}))"

    @staticmethod
    def GenSeperator(length: int = 32) -> str:
        # TODO resolve this
        # ? Pointless check and param either add as obfuscationlegacy param or remove
        if length < 12:
            raise Exception("Too short separator")
        return ''.join(choice(ascii_letters+digits) for _ in range(length))
