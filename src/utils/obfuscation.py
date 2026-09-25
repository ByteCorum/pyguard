from random import choice, randint
from string import ascii_letters, digits
from utils.crypto import FernetCipher, AesCipher, ChaCha20Cipher, Salsa20Cipher, compress, b64encode
import ast
from hashlib import sha256
from os import makedirs, getcwd, chdir, remove, rename, walk
from shutil import rmtree
from subprocess import run, PIPE, DEVNULL
from config import NAME, VERSION, AUTHOR
from utils.logger import Log

class MainObfuscation:
    def __init__(self, hashdata: bool, fernet: bool, aes: bool,
                chacha20: bool, salsa20: bool, base64: bool,
                recursive: int, noProtect: bool, encExec: bool) -> None:
        self.hashdata = hashdata
        self.fernet = fernet
        self.aes = aes
        self.chacha20 = chacha20
        self.salsa20 = salsa20
        self.base64 = base64
        self.noProtect = noProtect
        self.encExec = encExec
        self.recursive = recursive
        if self.recursive < 0:
            raise Exception("Invalid recursive value.")

        self.PrepareKeys()

    def PrepareKeys(self) -> None:
        self.number = randint(10000000,99999999)

        if self.hashdata:
            self.hashedVariables = []
        if not self.noProtect:
            self.files = []
        if self.fernet:
            self.fernetKey = FernetCipher.GenKey()
        if self.aes:
            self.aesKey = AesCipher.GenKey(256)
        if self.chacha20:
            self.chacha20Key = ChaCha20Cipher.GenKey()
        if self.salsa20:
            self.salsa20Key = Salsa20Cipher.GenKey()

    def Obfuscate(self, content: str) -> bytes:
        if self.hashdata:
            content = self.HashVariables(content)

        content = content.encode('utf-8')
        content = compress(content)
        content = content[::-1]
        if self.base64:
            content = b64encode(content)
            content = compress(content)

        if self.fernet:
            content = FernetCipher.Encrypt(self.fernetKey, content)
            content = compress(content)

        if self.aes:
            content = AesCipher.Encrypt(self.aesKey, content)
            content = compress(content)

        if self.chacha20:
            content = ChaCha20Cipher.Encrypt(self.chacha20Key, content)
            content = compress(content)

        if self.salsa20:
            content = Salsa20Cipher.Encrypt(self.salsa20Key, content)
            content = compress(content)

        for i in range(self.recursive):
            content = b64encode(content)
            content = content[::-1]
            content = compress(content)

        content = content[::-1]
        if self.base64:
            content = b64encode(content)
            content = compress(content)

        return content

    def HashVariables(self, content: str) -> str:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                string = node.value

                if len(string) > 1 and (any(char in ascii_letters for char in string) or any(char in digits for char in string)):
                    hashstr = sha256(string.encode('utf-8')).hexdigest()
                    compressedString = compress(string.encode('utf-8'))

                    if [hashstr,compressedString] not in self.hashedVariables:
                        self.hashedVariables.append([hashstr,compressedString])
                    content = content.replace(string, hashstr,1)

        return content

    def Wrap(self, content: bytes) -> str:
        content = f'''#Obfuscated by {NAME} {VERSION}
from DotPyGuard.script_{self.number} import DotPyGuard, _
_(DotPyGuard({content}, __file__)._)'''

        return content

    def ProtectFile(self, outputDir, filepath):
        if self.noProtect:
            return

        while filepath.startswith(('\\', '/')):
            filepath = filepath[1:]

        with open(f"{outputDir}/{filepath}", "rb") as file:
            fileHash = sha256(file.read()).hexdigest()

            if [filepath, fileHash] not in self.files:
                self.files.append([filepath, fileHash])

    def CreateExecutor(self, outputDir):
        secret = sha256(''.join(choice(ascii_letters+digits) for _ in range(randint(16,32))).encode("utf-8")).hexdigest()
        context = f'''
{'''from hashlib import sha256
from os import path, getcwd''' if not self.noProtect else ""}
{"from Crypto.Cipher import ChaCha20" if self.chacha20 else ""}
{"from Crypto.Cipher import Salsa20" if self.salsa20 else ""}
{"from cryptography.hazmat.primitives.ciphers.aead import AESGCM" if self.aes else ""}
{"from cryptography.fernet import Fernet" if self.fernet else ""}

from base64 import b64decode, b64encode
from zlib import decompress
from sys import exit

_ = exec

class DotPyGuard:
    def __init__(self, code, file):
        try:
            self.__code{secret} = code
            self.__file{secret} = file
            code = None
            file = None

            {f"self.__CheckHash{secret}()" if not self.noProtect else ""}
            self.__Decrypt{secret}()
        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)

    def __dir__(self) -> list[str]:
        return []

{f'''    def __CheckHash{secret}(self):
        try:
            self.__file{secret} = path.relpath(self.__file{secret}, getcwd())

            with open(self.__file{secret}, 'rb') as file:
                fileHash = sha256(file.read()).hexdigest()

            for file in {self.files}:
                if path.samefile(self.__file{secret}, file[0]) and fileHash == file[1]:
                    self.__file{secret} = None
                    return

            raise Exception("Invalid file hash")
        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)''' if not self.noProtect else ""}

    def __Decrypt{secret}(self):
        try:
            {f"self.__Base64{secret}()" if self.base64 else ""}
            self.__code{secret} = self.__code{secret}[::-1]
            {f"self.__Recursive{secret}()" if self.recursive else ""}
            {f"self.__Salsa{secret}()" if self.salsa20 else ""}
            {f"self.__ChaCha{secret}()" if self.chacha20 else ""}
            {f"self.__Aes{secret}()" if self.aes else ""}
            {f"self.__Fernet{secret}()" if self.fernet else ""}
            {f"self.__Base64{secret}()" if self.base64 else ""}

            self.__code{secret} = self.__code{secret}[::-1]
            self.__code{secret} = decompress(self.__code{secret})
            self.__code{secret} = self.__code{secret}.decode('utf-8')

            {f"self.__ReturnVariables{secret}()" if self.hashdata else ""}
            self.__code{secret} = b64encode(self.__code{secret}.encode('utf-8'))

        except Exception as runTimeError:
            print("Runtime error occurred, error: " + str(runTimeError))
            exit(-1)

    @property
    def _(self):
        return compile(b64decode(self.__code{secret}).decode('utf-8'), '<string>', 'exec')

{f'''    def __Recursive{secret}(self):
        for i in range({self.recursive}):
            self.__code{secret} = decompress(self.__code{secret})
            self.__code{secret} = self.__code{secret}[::-1]
            self.__code{secret} = b64decode(self.__code{secret})''' if self.recursive else ""}

{f'''    def __Salsa{secret}(self):
        self.__code{secret} = decompress(self.__code{secret})
        self.__code{secret} = b64decode(self.__code{secret})
        nonce = self.__code{secret}[:8]
        self.__code{secret} = self.__code{secret}[8:]
        self.__code{secret} = Salsa20.new(key={self.salsa20Key}, nonce=nonce).decrypt(self.__code{secret})'''
        if self.salsa20 else ""}

{f'''    def __ChaCha{secret}(self):
        self.__code{secret} = decompress(self.__code{secret})
        self.__code{secret} = b64decode(self.__code{secret})
        nonce = self.__code{secret}[:8]
        self.__code{secret} = self.__code{secret}[8:]
        self.__code{secret} = ChaCha20.new(key={self.chacha20Key}, nonce=nonce).decrypt(self.__code{secret})'''
        if self.chacha20 else ""}

{f'''    def __Aes{secret}(self):
        self.__code{secret} = decompress(self.__code{secret})
        aes = AESGCM({self.aesKey})
        self.__code{secret} = b64decode(self.__code{secret})
        nonce = self.__code{secret}[:12]
        self.__code{secret} = self.__code{secret}[12:]
        self.__code{secret} = aes.decrypt(nonce, self.__code{secret}, associated_data=None)''' if self.aes else ""}

{f'''    def __Fernet{secret}(self):
        self.__code{secret} = decompress(self.__code{secret})
        fernet = Fernet({self.fernetKey})
        self.__code{secret} = fernet.decrypt(self.__code{secret})''' if self.fernet else ""}

{f'''    def __Base64{secret}(self):
        self.__code{secret} = decompress(self.__code{secret})
        self.__code{secret} = b64decode(self.__code{secret})''' if self.base64 else ""}

{f'''    def __ReturnVariables{secret}(self):
        for raw in {self.hashedVariables}:
            string = decompress(raw[1]).decode("utf-8")
            self.__code{secret} = self.__code{secret}.replace(raw[0], string)''' if self.hashdata else ""}
'''
        outputDir =f"{outputDir}/DotPyGuard"
        makedirs(outputDir)

        if self.encExec:
            obfuscator = LegacyObfuscation(3, 6, LegacyObfuscation.GenSeperator())
            context = obfuscator.Encrypt(context)
            context = obfuscator.Wrap(context)

        with open(f"{outputDir}/script_{self.number}.py", "w", encoding="utf-8") as file:
            file.write(context)

        Log.Info(f"Executor script_{self.number}.py saved in {outputDir}")
        self.AssembleExecutor(outputDir)

    def AssembleExecutor(self, dir: str):
        code = f'''from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("script_{self.number}", ["script_{self.number}.py"]),
]

setup(
    name='.PyGuard',
    version='{VERSION}',
    author='{AUTHOR}',
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={{
            'language_level': "3",
            'binding': False,
            'embedsignature': False,
        }}
    )
)
'''

        with open(f"{dir}/assembler.py", "w", encoding="utf-8") as file:
            file.write(code)

        cur = getcwd()
        chdir(dir)

        Log.Info(f"Assembling executor...")
        result = run(["python", "assembler.py", "build_ext", "--inplace"],
                    stdout=Log.logFile if Log.logFile else DEVNULL,
                    stderr=PIPE, text=True)
        if result.stderr:
            Log.Fail(result.stderr.strip(), True)

        chdir(cur)
        rmtree(f"{dir}/build",ignore_errors=True)
        try:
            remove(f"{dir}/assembler.py")
            remove(f"{dir}/script_{self.number}.py")
            remove(f"{dir}/script_{self.number}.c")
        except:
            pass

        for dirpath, _, filenames in walk(dir):
            for filename in filenames:
                if filename.endswith(".pyd"):
                    rename(dirpath+"/"+filename, f'{dirpath}/script_{self.number}.pyd')

        Log.Info(f"Executor script_{self.number}.pyd assembled in {dir}")

class LegacyObfuscation:
    def __init__(self, mode, loops, separator: str):
        if mode < 1 or mode > 4:
            raise Exception("Invalid mode value.")
        if loops < 1:
            raise Exception("Invalid loops value.")

        self.mode = mode
        self.loops = loops
        self.separator = separator

    def Encrypt(self, content) -> str:
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
                    raise Exception("Invalid mode value.")

        return content

    def Wrap(self, content) -> str:
        match self.mode:
            case 1:
                return f"#Obfuscated by {NAME} {VERSION}\n_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode((__import__('zlib').decompress(__))[::-1])[::-1]);"+content
            case 2:
                return f"#Obfuscated by {NAME} {VERSION}\n_=lambda __:__import__('zlib').decompress(__import__('cryptography.fernet').fernet.Fernet(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1]).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])[::-1]);"+content
            case 3:
                return f"#Obfuscated by {NAME} {VERSION}\n_=lambda __:__import__('zlib').decompress(__import__('cryptography.fernet').fernet.Fernet(__import__('base64').b64decode(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1])).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])[::-1]);"+content
            case 4:
                return f"#Obfuscated by {NAME} {VERSION}\n_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode(__import__('zlib').decompress((__import__('cryptography.fernet').fernet.Fernet(__import__('base64').b64decode(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[1])).decrypt(((__import__('zlib').decompress(__))[::-1].split(b'{self.separator}'))[0])))[::-1]));"+content
            case _:
                raise Exception("Invalid mode value.")

    def PowerObfuscateion(self, content):
        content = content.encode('utf-8')
        content = compress(content)
        enccontent = b64encode(content)
        enccontent = enccontent[::-1]
        enccontent = compress(enccontent)

        key = FernetCipher.GenKey()
        enccontent = FernetCipher.Encrypt(key,enccontent)+self.separator.encode("utf-8")+b64encode(key)

        enccontent = enccontent[::-1]
        enccontent = compress(enccontent)

        return f"exec((_)({enccontent}))"

    def MediumObfuscation(self,content):
        content = content.encode('utf-8')
        content = compress(content)
        content = content[::-1]

        key = FernetCipher.GenKey()
        enccontent = FernetCipher.Encrypt(key, content)+self.separator.encode("utf-8")+b64encode(key)

        enccontent = enccontent[::-1]
        enccontent = compress(enccontent)

        return f"exec((_)({enccontent}))"

    def NormalObfuscation(self,content):
        content = content.encode('utf-8')
        content = compress(content)
        content = content[::-1]

        key = FernetCipher.GenKey()
        enccontent = FernetCipher.Encrypt(key, content)+self.separator.encode("utf-8")+key

        enccontent = enccontent[::-1]
        enccontent = compress(enccontent)

        return f"exec((_)({enccontent}))"

    def LiteObfuscation(self,content):
        content = content.encode('utf-8')
        content = compress(content)
        content = content[::-1]

        enccontent = b64encode(content)

        enccontent = enccontent[::-1]
        enccontent = compress(enccontent)

        return f"exec((_)({enccontent}))"

    @staticmethod
    def GenSeperator(length = 32):
        if length < 12:
            raise Exception("Too short separator")
        return ''.join(choice(ascii_letters+digits) for _ in range(length))