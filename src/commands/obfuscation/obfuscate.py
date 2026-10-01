from typing import override
from os import path, walk, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.langMgr import RemoveComments, GetImports
from utils.obfuscation import MainObfuscation

class Obfuscate(Command):
    exclusiveOptions: list[str | list[str]] = []
    requiredOptions: list[str | list[str]] = ["entrypoint", ["--hashdata", "--fernet", "--aes", "--chacha" "--base64", "--recursive"]]
    options: dict[str , bool | int | str | list[str]] = {
        "--quiet": False,
        "--log": "",
        "--no-color": False,
        "--no-input": False,

        "--hashdata": False,
        "--fernet": False,
        "--aes": False,
        "--chacha": False,
        "--base64": False,
        "--recursive": 0,

        "--no-integrity": False,
        "--enc-exec" : False,
        "--follow-imports" : False,
        "--debug-error": False,
        "--debug": False,
        "--decoy": "",

        "--dirs": [],
        "--files": [],
        "--output": "",

        "entrypoint": ""
    }

    help = f'''
Usage:
  pyguard obfuscate [options] <entry>
Example:
  pyguard obfuscate --hashdata --aes --follow-imports --decoy decoy.py main.py

Options:
  --help            -> get help for commands
  --quiet           -> give less output
  --log <path>      -> duplicate all logs to a file
  --no-color        -> suppress colored output
  --no-input        -> disable prompting for input

  --hashdata        -> replace all stings in code with sha512 hash
  --fernet          -> encrypt code using Fernet
  --aes             -> encrypt code using AES-GCM-SIV
  --chacha          -> encrypt code using XChaCha20-Poly1305
  --base64          -> encode entry and exit code with base64
  --recursive <num> -> fast recursive approach to prevent antivirus detection

  --no-integrity    -> disable file integrity checks
  --enc-exec        -> obfuscate executor using legacy method; may weaken security
  --follow-imports  -> add all imports to the protected script to make building easy
  --debug-error     -> development builds only; executor will give verbose errors
  --debug           -> development builds only; executor will skip environment checks
  --decoy <path>    -> code to execute if execution environment marks as hostile

  --dirs <path>     -> selected dirs for obfuscation
  --files <path>    -> selected files for obfuscation
  --output <path>   -> output dir path

Note:
  Syntax:
    text,text         -> to add more than one arg to option
    <name>.py         -> the entry point of your program in the end of command

  Required options:
    entry point in the end of command

  Required at least 1 of those options:
    --hashdata, --fernet, --aes, --chacha, --base64, --recursive
'''

    def __init__(self) -> None:
        Log.Info("Obfuscation")

        self.InitVars()
        try:
            self.ValidateParams()
        except TypeError as error:
            raise TypeError("Parameter validation error: internal error: " + str(error)) from error
        except ValueError as error:
            raise ValueError("Parameter validation error: " + str(error)) from error

        try:
            self.ObfuscateFiles()
            # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams, self.options["--output"] can only be str
            self.obfuscation.CreateExecutor(self.options["--output"])
        except Exception as error:
            raise Exception("Execution error: " + str(error)) from error

        Log.Success("Obfuscation completed", bypassQuiet=True)

    def InitVars(self) -> None:
        self.decoySource = ""
        self.projRoot:str
        self.imports: list[str] = []

    @override
    def ValidateParams(self) -> None:
        # Bool Params
        ## Options
        if type(self.options["--follow-imports"]) != bool:
            raise TypeError(f"invalid \"--follow-imports\" variable type: must be \"bool\", but it's \"{type(self.options["--follow-imports"])}\"")
        if self.options["--follow-imports"]:
            Log.Info("Follow imports: Enabled")

        if type(self.options["--no-integrity"]) != bool:
            raise TypeError(f"invalid \"--no-integrity\" variable type: must be \"bool\", but it's \"{type(self.options["--no-integrity"])}\"")
        if self.options["--no-integrity"]:
            Log.Warning("File integrity checks: Disabled")

        if type(self.options["--enc-exec"]) != bool:
            raise TypeError(f"invalid \"--enc-exec\" variable type: must be \"bool\", but it's \"{type(self.options["--enc-exec"])}\"")
        if self.options["--enc-exec"]:
            Log.Info("Executor obfuscation: Enabled")

        if type(self.options["--debug-error"]) != bool:
            raise TypeError(f"invalid \"--debug-error\" variable type: must be \"bool\", but it's \"{type(self.options["--debug-error"])}\"")
        if self.options["--debug-error"]:
            Log.Warning("Executor verbose errors: Enabled")

        if type(self.options["--debug"]) != bool:
            raise TypeError(f"invalid \"--debug\" variable type: must be \"bool\", but it's \"{type(self.options["--debug"])}\"")
        if self.options["--debug"]:
            Log.Warning("Executor debug build: Enabled")

        ## Methods
        if type(self.options["--hashdata"]) != bool:
            raise TypeError(f"invalid \"--hashdata\" variable type: must be \"bool\", but it's \"{type(self.options["--hashdata"])}\"")
        if self.options["--hashdata"]:
            Log.Info("Hashing of strings: Enabled")

        if type(self.options["--fernet"]) != bool:
            raise TypeError(f"invalid \"--fernet\" variable type: must be \"bool\", but it's \"{type(self.options["--fernet"])}\"")
        if self.options["--fernet"]:
            Log.Info("Fernet encryption: Enabled")

        if type(self.options["--aes"]) != bool:
            raise TypeError(f"invalid \"--aes\" variable type: must be \"bool\", but it's \"{type(self.options["--aes"])}\"")
        if self.options["--aes"]:
            Log.Info("AES-GCM-SIV encryption: Enabled")

        if type(self.options["--chacha"]) != bool:
            raise TypeError(f"invalid \"--chacha\" variable type: must be \"bool\", but it's \"{type(self.options["--chacha"])}\"")
        if self.options["--chacha"]:
            Log.Info("XChaCha20-Poly1305 encryption: Enabled")

        if type(self.options["--base64"]) != bool:
            raise TypeError(f"invalid \"--base64\" variable type: must be \"bool\", but it's \"{type(self.options["--base64"])}\"")
        if self.options["--base64"]:
            Log.Info("Base64 encoding: Enabled")

        # Val Params
        if type(self.options["--recursive"]) != int:
            raise TypeError(f"invalid \"--recursive\" variable type: must be \"int\", but it's \"{type(self.options["--recursive"])}\"")
        if self.options["--recursive"] < 0:
            raise TypeError("Invalid --recursive value")
        if self.options["--recursive"] > 0:
            Log.Info(f"Recursive approach loops: {self.options["--recursive"]}")

        if type(self.options["--decoy"]) != str:
            raise TypeError(f"invalid \"--decoy\" variable type: must be \"str\", but it's \"{type(self.options["--decoy"])}\"")
        decoyfile:str = self.options["--decoy"]
        if decoyfile:
            if not path.exists(decoyfile) or not path.isfile(decoyfile) or not decoyfile.endswith(".py"):
                    raise ValueError(f"Invalid decoy file path: {decoyfile}")

            with open(decoyfile, "r", encoding="utf-8") as pyFile:
                self.decoySource:str = pyFile.read()
            if not self.decoySource:
                raise ValueError(f"Decoy file {decoyfile} is empty")

            Log.Info(f"Decoy code loaded from: {decoyfile}")

        Log.Custom("",end='\n')# Separator

        # Program Entry File
        if type(self.options["entrypoint"]) != str:
            raise TypeError(f"invalid entrypoint path type: must be \"str\", but it's \"{type(self.options["entrypoint"])}\"")

        self.entryPoint:str = self.options["entrypoint"]
        if not path.exists(self.entryPoint) or not path.isfile(self.entryPoint) or not self.entryPoint.endswith(".py"):
            raise ValueError(f"Invalid entry file path: {self.entryPoint}")

        self.entryPoint = path.abspath(self.entryPoint)
        Log.Info(f"Entry file: {self.entryPoint}")

        # Files Check
        if type(self.options["--files"]) != list:
            raise TypeError(f"invalid \"--files\" variable type: must be \"list\", but it's \"{type(self.options["--files"])}\"")

        for i in range (len(self.options["--files"])):
            file:str = self.options["--files"][i]
            if not path.exists(file) or not path.isfile(file) or not file.endswith(".py"):
                raise ValueError(f"Invalid file path: {file}")

            self.options["--files"][i] = path.abspath(file)
            Log.Info(f"Included file: {self.options["--files"][i]}")

        # Dirs Check
        if type(self.options["--dirs"]) != list:
            raise TypeError(f"invalid \"--dirs\" variable type: must be \"list\", but it's \"{type(self.options["--dirs"])}\"")

        for i in range(len(self.options["--dirs"])):
            dir:str = self.options["--dirs"][i]
            if not path.exists(dir) or not path.isdir(dir):
                raise ValueError(f"Invalid directory path: {dir}")

            self.options["--dirs"][i] = path.abspath(dir)
            Log.Info(f"Included dir: {self.options['--dirs'][i]}")

        # Common dir to determinate where to place output dir
        # Basically project root location
        if len(self.options["--files"]) == 0 and len(self.options["--dirs"]) == 0:
            # commonpath returns the file itself when there's exactly one path, so strip the filename manually
            self.projRoot = path.dirname(self.entryPoint)
        else:
            allPaths: list[str] = self.options["--files"]+self.options["--dirs"]+[self.entryPoint]
            self.projRoot = path.commonpath(allPaths) #Example of projRoot: /home/usr/python/pyguard/examples/complex-legacy/

        pathParts: list[str] = self.projRoot.split(path.sep)
        if self.projRoot == path.sep or len(pathParts) <= 2:
            Log.Warning(f"Computed common root \"{self.projRoot}\" is suspiciously shallow; the paths appear to come from unrelated trees", pause=True)

        # Output dir
        if type(self.options["--output"]) != str:
            raise TypeError(f"invalid \"--output\" variable type: must be \"str\", but it's \"{type(self.options["--output"])}\"")
        if not self.options["--output"]:
            self.options["--output"] = "obfuscated"

        self.options["--output"] = path.join(self.projRoot, self.options["--output"])
        if path.exists(self.options["--output"]):
            Log.Warning(f"Output directory already exists: {self.options["--output"]}")

            response = ""
            while response != "y" and response != "n" and response != "ignored":
                response:str = Log.Question("Override directory? (y/n)").lower()

                match response:
                    case "ignored":
                        rmtree(self.options["--output"])
                        Log.Info("Directory overridden")
                        break

                    case "y":
                        rmtree(self.options["--output"])
                        Log.Success("Directory overridden")
                        break

                    case "n":
                        Log.Success("Directory skipped")
                        break

                    case _:
                        Log.Fail("Invalid response. Please enter 'y' or 'n'")

        Log.Info(f"Output dir: {self.options["--output"]}")
        Log.Custom("",end='\n')# Separator

    def ObfuscateFiles(self) -> None:
        # pyrefly: ignore [bad-argument-type] - all those were already checked in ValidateParams
        self.obfuscation = MainObfuscation(self.options["--hashdata"], self.options["--fernet"], self.options["--aes"], self.options["--chacha"], self.options["--base64"], self.options["--recursive"], self.options["--no-integrity"], self.options["--enc-exec"], self.options["--debug-error"], self.options["--debug"], self.decoySource)

        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--files"] can only be list[str]
        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                content:str = pyFile.read()
            if not content:
                Log.Warning(f"File {file} is empty")
                continue

            content = RemoveComments(content)
            self.FollowImports(content)

            encBytes:bytes = self.obfuscation.Obfuscate(content)
            content = self.obfuscation.Wrap(encBytes)

            # Check description of relfilepath in entryPoint section below
            relfilepath:str = path.normpath(path.relpath(file, self.projRoot)) # relfilepath -> path to file in project
            self.SaveFile(relfilepath, content)
            # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams, self.options["--output"] can only be str
            self.obfuscation.ProtectFileModifications(relfilepath, self.options["--output"])

        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--dirs"] can only be list[str]
        for dir in self.options["--dirs"]:
            for dirpath_, dirnames_, filenames_ in walk(dir):
                for filename in filenames_:
                    file:str = path.join(dirpath_, filename)
                    if filename.lower().endswith(".py"):
                        with open(file, "r", encoding="utf-8") as pyFile:
                            content: str = pyFile.read()
                        if not content:
                            Log.Warning(f"File {file} is empty")
                            continue
                    else:
                        Log.Warning(f"File {file} is skipped as it's not python file")
                        continue

                    content = RemoveComments(content)
                    self.FollowImports(content)

                    encBytes:bytes = self.obfuscation.Obfuscate(content)
                    content = self.obfuscation.Wrap(encBytes)

                    # Check description of relfilepath in entryPoint section below
                    relfilepath:str = path.normpath(path.relpath(file, self.projRoot)) # relfilepath -> path to file in project
                    self.SaveFile(relfilepath, content)
                    # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams, self.options["--output"] can only be str
                    self.obfuscation.ProtectFileModifications(relfilepath, self.options["--output"])

        with open(self.entryPoint, "r", encoding="utf-8") as pyFile:
            content:str = pyFile.read()
        if not content:
            raise ValueError(f"File {self.entryPoint} is empty") # entry point must exist

        content = RemoveComments(content)
        self.FollowImports(content)

        encBytes:bytes = self.obfuscation.Obfuscate(content)
        content = self.obfuscation.Wrap(encBytes)

        # filepath: /home/usr/python/pyguard/examples/complex-legacy/main.py
        # projRoot: /home/usr/python/pyguard/examples/complex-legacy/
        # relfilepath: main.py

        # filepath: /home/usr/python/pyguard/examples/complex-legacy/dir/dir/result.py
        # projRoot: /home/usr/python/pyguard/examples/complex-legacy/
        # relfilepath: dir/dir/result.py

        relfilepath:str = path.normpath(path.relpath(self.entryPoint, self.projRoot)) # relfilepath -> path to file in project
        self.SaveFile(relfilepath, content, entry=True)
        # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams, self.options["--output"] can only be str
        self.obfuscation.ProtectFileModifications(relfilepath, self.options["--output"])

    def SaveFile(self, relfilepath: str, content: str, entry:bool = False) -> None:
        imports = ""
        if entry:
            for module in self.imports:
                imports+=f"import {module}\n"
            content = imports + content

        # pyrefly: ignore [no-matching-overload] - already checked in ValidateParams, self.options["--output"] can only be str
        filepath = path.normpath(path.join(self.options["--output"], relfilepath))
        # filepath: projRoot(/home/usr/python/pyguard/examples/complex-legacy/) + obfuscated + relpath(./dir/dir) => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/./dir/dir => normpath => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/dir/dir
        makedirs(path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"File {path.basename(filepath)} saved as {filepath}")

    def FollowImports(self, content: str) -> None:
        if self.options["--follow-imports"]:
            modules:list[str] = GetImports(content)

            if not self.options["--no-integrity"]:
                modules += ["hashlib", "os"]

            if self.options["--chacha"]:
                modules.append("Crypto.Cipher")

            if self.options["--aes"]:
                modules.append("cryptography.hazmat.primitives.ciphers.aead")

            if self.options["--fernet"]:
                modules.append("cryptography.fernet")

            modules += ["sys", "base64", "zlib"]

            #Fight duplicates
            for module in modules:
                if not module in self.imports:
                    self.imports.append(module)
