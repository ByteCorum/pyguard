from shutil import rmtree
from subprocess import run, PIPE, DEVNULL
import ast
from random import choice, randint
from string import ascii_letters, digits
from zlib import compress
from hashlib import sha512
from os import path, makedirs, remove, listdir, rename
import sys
import re
from typing import override
from base64 import b64encode
from utils.crypto import FernetMethod, AesGcmSivMethod, XChaCha20Poly1305Method
from utils.legacyObfuscation import LegacyObfuscation
from config import NAME, VERSION, AUTHOR, EXECUTOR_TEMPLATE
from utils.logger import Log

class MainObfuscation:
    def __init__(self, hashdata: bool, fernet: bool, aes: bool,
                chacha: bool, base64: bool,
                recursive: int, noProtect: bool, encExec: bool) -> None:

        self.hashdata: bool = hashdata
        self.fernet: bool = fernet
        self.aes: bool = aes
        self.chacha: bool = chacha
        self.base64: bool = base64
        self.noProtect: bool = noProtect
        self.encExec: bool = encExec
        self.debug: bool = False
        self.recursive: int = recursive
        self.decoySource: str = ""

        if self.recursive < 0:
            raise Exception("Invalid recursive value")

        self.InitVars()
        self.GenKeys()

    def InitVars(self) -> None:
        self.number: int = randint(1000000000, 9999999999)
        self.executorDir: str = "pyguard"
        self.executorFile: str = f"script_{self.number}.py"
        self.assemblerFile: str = f"assembler.py"

        if self.hashdata:
            # Maps SHA-512 digest -> compressed original string
            self.hashedVariables: dict[str, bytes] = {}

        if not self.noProtect:
            # Maps relpath to file from pyguard executor -> SHA-512 digest
            self.files: dict[str, str] = {}

    def GenKeys(self) -> None:
        if self.fernet:
            self.fernetKey: bytes = FernetMethod.GenKey()
        if self.aes:
            self.aesKey: bytes = AesGcmSivMethod.GenKey(256)
        if self.chacha:
            self.chachaKey: bytes = XChaCha20Poly1305Method.GenKey()

    def Obfuscate(self, content: str) -> bytes:
        if self.hashdata:
            content = self.HashVariables(content)

        bytestr:bytes = content.encode('utf-8')
        bytestr = compress(bytestr)
        bytestr = bytestr[::-1]

        if self.base64:
            bytestr = b64encode(bytestr)
            bytestr = compress(bytestr)

        if self.fernet:
            bytestr = FernetMethod.Encrypt(self.fernetKey, bytestr)
            bytestr = compress(bytestr)

        if self.aes:
            bytestr = AesGcmSivMethod.Encrypt(self.aesKey, bytestr)
            bytestr = compress(bytestr)

        if self.chacha:
            bytestr = XChaCha20Poly1305Method.Encrypt(self.chachaKey, bytestr)
            bytestr = compress(bytestr)

        for i in range(self.recursive):
            bytestr = b64encode(bytestr)
            bytestr = bytestr[::-1]
            bytestr = compress(bytestr)

        bytestr = bytestr[::-1]

        if self.base64:
            bytestr = b64encode(bytestr)
            bytestr = compress(bytestr)

        return bytestr

    class __VariableHasher(ast.NodeTransformer):
        def __init__(self, hashed: dict[str, bytes]) -> None:
            self.hashed = hashed

        @staticmethod
        def __is_interesting(s: str) -> bool:
            # More than one character and containing at least one letter or one digit (excludes, for example, "," or " " alone).
            return len(s) > 1 and any(
                c in ascii_letters or c in digits for c in s
            )

        @override
        def visit_Constant(self, node: ast.Constant) -> ast.Constant:
            if isinstance(node.value, str) and self.__is_interesting(node.value):
                raw:bytes = node.value.encode('utf-8')
                digest:str = sha512(raw).hexdigest()

                # setdefault guarantees idempotency: if this exact string was already seen, the stored entry is kept and compress() is not executed again
                self.hashed.setdefault(digest, compress(raw))
                node.value = digest
            return node

    def HashVariables(self, content: str) -> str:
        try:
            tree: ast.Module = ast.parse(content)
        except SyntaxError as error:
            raise ValueError(f"Source is not valid Python: {error}") from error

        # __VariableHasher overrides default behavior of visit
        tree = self.__VariableHasher(self.hashedVariables).visit(tree)
        # Fills in missing lineno and col_offset attributes on modified nodes. Node replacement can leave location metadata inconsistent.
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def Wrap(self, content: bytes) -> str:
        return f"#Obfuscated by {NAME}\nfrom pyguard.script_{self.number} import PyGuard, _\n_(PyGuard({content}, __file__)._)"

    #relfilepath -> path to file in project
    def ProtectFileModifications(self, relfilepath: str, outputDir: str) -> None:
        if self.noProtect:
            return

        filepath: str = path.normpath(path.join(outputDir, relfilepath))
        executorPath: str = path.normpath(path.join(outputDir, self.executorDir, self.executorFile))
        fromExecToFile: str = path.relpath(filepath, path.dirname(executorPath))

        with open(filepath, "rb") as file:
            fileHash:str = sha512(file.read()).hexdigest()

        self.files[fromExecToFile] = fileHash

    def Inject(self, content: str, needle: str, replacement: str, what: str) -> str:
        if content.count(needle) != 1:
            raise Exception(f"Executor injection failed: {what} (expected exactly 1 marker, found {content.count(needle)})")
        return content.replace(needle, replacement, 1)


    def StripDisabledLayers(self, executorContent: str, postfix: str) -> str:
        #A disabled layer must leave no trace at all: a dead `if _flag: self.__Stage(...)` call would hand an analyst the stage names and framing hints of layers this build never uses
        content: str = executorContent

        def stripMethod(name: str) -> None:
            nonlocal content
            pattern: str = (r"\n        def __" + name + re.escape(postfix)
                            + r"\(self.*?(?=\n        def )")
            content, count = re.subn(pattern, "", content, count=1, flags=re.DOTALL)
            if count != 1:
                raise Exception(f"Executor strip failed: {name} stage not found")

        def stripLine(line: str) -> None:
            nonlocal content
            if content.count(line + "\n") != 1:
                raise Exception(f"Executor strip failed: import not found: {line}")
            content = content.replace(line + "\n", "", 1)

        def stripFlag(flag: str) -> None:
            nonlocal content
            kept = [l for l in content.split("\n")
                    if not l.startswith(f"_{flag}{postfix}:")]
            if len(kept) == len(content.split("\n")):
                raise Exception(f"Executor strip failed: flag {flag} not found")
            content = "\n".join(kept)

        def stripGuardBlock(guardLine: str, callLine: str, expected: int = 1) -> None:
            nonlocal content
            needle: str = guardLine + "\n" + callLine + "\n"
            count: int = content.count(needle)
            if count != expected:
                raise Exception(f"Executor strip failed: guard block not found ({count}/{expected})")
            content = content.replace(needle, "")

        if self.noProtect:
            stripMethod("CheckFileIntegrity")
            stripLine("from hashlib import sha512")
            stripLine("from os import path")
            stripFlag("integrityEnabled")
            stripGuardBlock(
                f"                if _integrityEnabled{postfix}:",
                f"                    self.__CheckFileIntegrity{postfix}(filepath)")

        if not self.base64:
            stripMethod("Base64")
            stripFlag("base64Enabled")
            stripGuardBlock(
                f"            if _base64Enabled{postfix}:",
                f"                _b = self.__Base64{postfix}(_b)", expected=2)

        if self.recursive <= 0:
            stripMethod("Recursive")
            stripFlag("recursiveIterations")
            stripGuardBlock(
                f"            if _recursiveIterations{postfix}:",
                f"                _b = self.__Recursive{postfix}(_b)")

        if not self.chacha:
            stripMethod("ChaCha")
            stripLine("from Crypto.Cipher import ChaCha20_Poly1305")
            stripFlag("chachaEnabled")
            stripGuardBlock(
                f"            if _chachaEnabled{postfix}:",
                f"                _b = self.__ChaCha{postfix}(_b)")

        if not self.aes:
            stripMethod("Aes")
            stripLine("from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV")
            stripFlag("aesEnabled")
            stripGuardBlock(
                f"            if _aesEnabled{postfix}:",
                f"                _b = self.__Aes{postfix}(_b)")

        if not self.fernet:
            stripMethod("Fernet")
            stripLine("from cryptography.fernet import Fernet")
            stripFlag("fernetEnabled")
            stripGuardBlock(
                f"            if _fernetEnabled{postfix}:",
                f"                _b = self.__Fernet{postfix}(_b)")

        # b64decode is used by __Base64, __Recursive, __ChaCha and __Aes; only when all four are gone may the import go too.
        if (not self.base64) and self.recursive <= 0 and (not self.chacha) and (not self.aes):
            stripLine("from base64 import b64decode")
        return content


    def CreateExecutor(self, outputDir: str) -> None:
        # Per-build random postfix
        postfix: str = sha512(''.join(choice(ascii_letters + digits) for _ in range(randint(64, 128))).encode("utf-8")).hexdigest()

        if not path.exists(EXECUTOR_TEMPLATE):
            raise Exception(f"Executor template {EXECUTOR_TEMPLATE} doesn't exist")
        with open(EXECUTOR_TEMPLATE, "r", encoding="utf-8") as executor:
            executorContent: str = executor.read()
        if not executorContent:
            raise Exception(f"Executor template {EXECUTOR_TEMPLATE} is empty")


        executorContent = executorContent.replace("SECRET", postfix)
        executorContent = self.StripDisabledLayers(executorContent, postfix)

        # Presence verification
        if not self.noProtect:
            executorContent = self.Inject(executorContent,
                                            f"_integrityEnabled{postfix}: bool = True",
                                            f"_integrityEnabled{postfix}: bool = True",
                                            "integrity switch")
        if self.base64:
            executorContent = self.Inject(executorContent,
                                            f"_base64Enabled{postfix}: bool = True",
                                            f"_base64Enabled{postfix}: bool = True",
                                            "base64 switch")
        if self.chacha:
            executorContent = self.Inject(executorContent,
                                            f"_chachaEnabled{postfix}: bool = True",
                                            f"_chachaEnabled{postfix}: bool = True",
                                            "chacha switch")
        if self.aes:
            executorContent = self.Inject(executorContent,
                                            f"_aesEnabled{postfix}: bool = True",
                                            f"_aesEnabled{postfix}: bool = True",
                                            "aes switch")
        if self.fernet:
            executorContent = self.Inject(executorContent,
                                            f"_fernetEnabled{postfix}: bool = True",
                                            f"_fernetEnabled{postfix}: bool = True",
                                            "fernet switch")

        #Manifests
        executorContent = self.Inject(executorContent,
                                        f"_filehashmanifest{postfix}: dict[str, str] = {{}}",
                                        f"_filehashmanifest{postfix}: dict[str, str] = {getattr(self, 'files', {})!r}",
                                        "file hash manifest")
        executorContent = self.Inject(executorContent,
                                        f"_literalmanifest{postfix}: dict[str, bytes] = {{}}",
                                        f"_literalmanifest{postfix}: dict[str, bytes] = {getattr(self, 'hashedVariables', {})!r}",
                                        "literal manifest")
        if self.recursive > 0:
            executorContent = self.Inject(executorContent,
                                            f"_recursiveIterations{postfix}: int = 0",
                                            f"_recursiveIterations{postfix}: int = {self.recursive}",
                                            "recursive iterations")

        # Keys
        if self.chacha:
            executorContent = self.Inject(executorContent,
                                            f'__chachaKey{postfix} = b""',
                                            f"__chachaKey{postfix} = {self.chachaKey!r}",
                                            "chacha key")
        if self.aes:
            executorContent = self.Inject(executorContent,
                                            f'__aesKey{postfix} = b""',
                                            f"__aesKey{postfix} = {self.aesKey!r}",
                                            "aes key")
        if self.fernet:
            executorContent = self.Inject(executorContent,
                                            f'__fernetKey{postfix} = b""',
                                            f"__fernetKey{postfix} = {self.fernetKey!r}",
                                            "fernet key")

        # Behaviour switches
        executorContent = self.Inject(executorContent,
                                        f"_DEBUG_BUILD_{postfix} = False",
                                        f"_DEBUG_BUILD_{postfix} = {self.debug}",
                                        "debug switch")
        decoy: str = self.decoySource or 'print("dome generic python error")'
        executorContent = self.Inject(executorContent,
                                        f'_DECOY_SOURCE_{postfix} = "\\n"',
                                        f"_DECOY_SOURCE_{postfix} = {decoy!r}",
                                        "decoy source")

        executorPath: str = path.join(outputDir, self.executorDir, self.executorFile)
        makedirs(path.dirname(executorPath), exist_ok=True)

        initPath: str = path.join(outputDir, self.executorDir, "__init__.py")
        with open(initPath, "w", encoding="utf-8") as initFile:
            initFile.write(f"# {NAME} {VERSION}\n__all__: list[str] = []\n") #The directory obfuscated/pyguard/ must be an importable package for the launcher statement from pyguard.script_1401026711 import PyGuard, _ to resolve.

        if self.encExec:
            obfuscator = LegacyObfuscation(3, 6, LegacyObfuscation.GenSeperator())
            executorContent = obfuscator.Encrypt(executorContent)
            executorContent = obfuscator.Wrap(executorContent)

        with open(executorPath, "w", encoding="utf-8") as file:
            file.write(executorContent)

        Log.Info(f"Executor saved as {executorPath}")
        self.AssembleExecutor(outputDir)


    def AssembleExecutor(self, outputDir: str) -> None:
        executorDirPath: str = path.join(outputDir, self.executorDir)
        assemblerPath: str = path.join(executorDirPath, self.assemblerFile)
        stem: str = self.executorFile[:-3]
        makedirs(executorDirPath, exist_ok=True)

        assembler: str = f'''from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("{stem}", ["{self.executorFile}"]),
]

setup(
    name='pyguard',
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
        with open(assemblerPath, "w", encoding="utf-8") as file:
            file.write(assembler)

        Log.Info("Assembling executor...")

        # pyrefly: ignore [no-matching-overload]
        result = run(
            args=[sys.executable, self.assemblerFile, "build_ext", "--inplace"],
            cwd=executorDirPath,
            stdout=Log.logFile if Log.logFile else DEVNULL,
            stderr=PIPE,
            text=True,
        )
        if result.returncode != 0 or result.stderr:
            rmtree(path.join(executorDirPath, "build"), ignore_errors=True)
            raise Exception(f"Executor assembly failed (exit code {result.returncode}): "
                     + (result.stderr.strip() or "compiler produced no diagnostics"))

        # Locate the platform-tagged extension
        # script_NNN.cpNNN-win_amd64.pyd on Windows,
        # script_NNN.cpython-NNN-<platform>.so elsewhere
        built = [
            name for name in listdir(executorDirPath)
            if name.startswith(stem) and (name.endswith(".pyd") or name.endswith(".so"))
        ]
        if not built:
            rmtree(path.join(executorDirPath, "build"), ignore_errors=True)
            raise Exception(f"Executor assembly produced no extension module for {stem}")
        built.sort(key=lambda name: path.getmtime(path.join(executorDirPath, name)), reverse=True)

        canonical: str = stem + (".pyd" if built[0].endswith(".pyd") else ".so")
        builtPath: str = path.join(executorDirPath, built[0])
        canonicalPath: str = path.join(executorDirPath, canonical)
        if path.exists(canonicalPath):
            remove(canonicalPath)
        if builtPath != canonicalPath:
            rename(builtPath, canonicalPath)

        # Remove intermediates. The .py source must be deleted so the import resolves to the extension only, never to readable source.
        rmtree(path.join(executorDirPath, "build"), ignore_errors=True)
        for intermediate in (self.assemblerFile, self.executorFile, f"{stem}.c"):
            try:
                remove(path.join(executorDirPath, intermediate))
            except OSError:
                pass

        Log.Info(f"Executor {canonical} assembled in {executorDirPath}")
