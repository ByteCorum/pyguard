from typing import override
from os import path, sep, walk, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.langMgr import RemoveComments, GetImports
from utils.obfuscation import MainObfuscation

class Obfuscate(Command):
    exclusiveOptions: list[str | list[str]] = []
    requiredOptions: list[str | list[str]] = ["entrypoint", ["--hashdata", "--fernet", "--aes", "--chacha", "--salsa" "--base64", "--recursive"]]
    options: dict[str , bool | int | str | list[str]] = {
        "--quiet": False,
        "--log": "",
        "--no-color": False,
        "--no-input": False,

        "--hashdata": False,
        "--fernet": False,
        "--aes": False,
        "--chacha": False,
        "--salsa": False,
        "--base64": False,
        "--recursive": 0,
        "--no-protect": False,
        "--enc-exec" : False,
        "--dirs": [],
        "--files": [],
        "--output": "",
        "--follow-imports" : False,
        "entrypoint": ""
    }

    help = f'''
Usage:
  pyguard obfuscate [options] <entry>.py
Example:
  pyguard obfuscate --hashdata --aes --follow-imports main.py

Notes:
  text,text         -> to add more than one arg to option
  main.py           -> the entry point of your program

Options:
  --help            -> show help for commands
  --quiet           -> give less output
  --log <path>      -> write all logs to a file
  --no-color        -> suppress colored output
  --no-input        -> disable prompting for input

  --hashdata        -> convert all strings and var names into hash
  --fernet          -> obfuscation and encryption using fernet
  --aes             -> obfuscation and encryption using aes256
  --chacha          -> obfuscation and encryption using chacha20
  --salsa           -> obfuscation and encryption using salsa20
  --base64          -> obfuscation and encryption using base64
  --recursive <num> -> not strong but good if u need to hide ur prog from AVs
  --no-protect      -> disable file modification protection
  --enc-exec        -> obfuscate executor via legacy encryption method
  --dirs <path>     -> obfuscate all files in dir
  --files <path>    -> files for obfuscation
  --output <path>   -> output dir
  --follow-imports  -> add all imports to the protected script'''

    def __init__(self) -> None:
        Log.Info("Obfuscation")

        self.InitVars()
        self.ValidateParams()
        self.ObfuscateFiles()
        self.obfuscation.CreateExecutor(self.options["--output"])

        Log.Success("Obfuscation completed", bypassQuiet=True)

    def InitVars(self) -> None:
        self.commonPath:str
        self.imports: list[str] = []

    @override
    def ValidateParams(self) -> None:
        # Bool Params
        ## Options
        if type(self.options["--follow-imports"]) != bool:
            raise Exception(f"invalid \"--follow-imports\" variable type: must be \"bool\", but it's \"{type(self.options["--follow-imports"])}\"")
        if self.options["--follow-imports"]:
            Log.Info(f"Follow imports: Enabled")

        if type(self.options["--no-protect"]) != bool:
            raise Exception(f"invalid \"--no-protect\" variable type: must be \"bool\", but it's \"{type(self.options["--no-protect"])}\"")
        if self.options["--no-protect"]:
            Log.Info(f"File modification protection: Disabled")

        if type(self.options["--enc-exec"]) != bool:
            raise Exception(f"invalid \"--enc-exec\" variable type: must be \"bool\", but it's \"{type(self.options["--enc-exec"])}\"")
        if self.options["--enc-exec"]:
            Log.Info(f"Executor encryption: Enabled")

        ## Methods
        if type(self.options["--hashdata"]) != bool:
            raise Exception(f"invalid \"--hashdata\" variable type: must be \"bool\", but it's \"{type(self.options["--hashdata"])}\"")
        if self.options["--hashdata"]:
            Log.Info(f"Hashing of strings and var names: Enabled")

        if type(self.options["--fernet"]) != bool:
            raise Exception(f"invalid \"--fernet\" variable type: must be \"bool\", but it's \"{type(self.options["--fernet"])}\"")
        if self.options["--fernet"]:
            Log.Info(f"Fernet encryption: Enabled")

        if type(self.options["--aes"]) != bool:
            raise Exception(f"invalid \"--aes\" variable type: must be \"bool\", but it's \"{type(self.options["--aes"])}\"")
        if self.options["--aes"]:
            Log.Info(f"AES-GCM encryption: Enabled")

        if type(self.options["--chacha"]) != bool:
            raise Exception(f"invalid \"--chacha\" variable type: must be \"bool\", but it's \"{type(self.options["--chacha"])}\"")
        if self.options["--chacha"]:
            Log.Info(f"ChaCha20 encryption: Enabled")

        if type(self.options["--salsa"]) != bool:
            raise Exception(f"invalid \"--salsa\" variable type: must be \"bool\", but it's \"{type(self.options["--salsa"])}\"")
        if self.options["--salsa"]:
            Log.Info(f"Salsa20 encryption: Enabled")

        if type(self.options["--base64"]) != bool:
            raise Exception(f"invalid \"--base64\" variable type: must be \"bool\", but it's \"{type(self.options["--base64"])}\"")
        if self.options["--base64"]:
            Log.Info(f"Base64 encoding: Enabled")

        # Val Params
        if type(self.options["--recursive"]) != int:
            raise Exception(f"invalid \"--recursive\" variable type: must be \"int\", but it's \"{type(self.options["--recursive"])}\"")
        if self.options["--recursive"] < 0:
            raise Exception("Invalid --recursive value")
        if self.options["--recursive"] > 0:
            Log.Info(f"Recursive obfuscation loops: {self.options["--recursive"]}")

        Log.Custom("",end='\n')# Separator

        # Program Entry File
        if type(self.options["entrypoint"]) != str:
            raise Exception(f"invalid entrypoint path type: must be \"str\", but it's \"{type(self.options["entrypoint"])}\"")

        self.entryPoint:str = self.options["entrypoint"]
        if not path.exists(self.entryPoint) or not path.isfile(self.entryPoint) or not self.entryPoint.endswith(".py"):
            raise Exception(f"Invalid entry file path: {self.entryPoint}")

        self.entryPoint = path.abspath(self.entryPoint)
        Log.Info(f"Entry file: {self.entryPoint}")

        # Files Check
        if type(self.options["--files"]) != list:
            raise Exception(f"invalid \"--files\" variable type: must be \"list\", but it's \"{type(self.options["--files"])}\"")

        for i in range (len(self.options["--files"])):
            file:str = self.options["--files"][i]
            if not path.exists(file) or not path.isfile(file) or not file.endswith(".py"):
                raise Exception(f"Invalid file path: {file}")

            self.options["--files"][i] = path.abspath(file)
            Log.Info(f"Included file: {self.options["--files"][i]}")

        # Dirs Check
        if type(self.options["--dirs"]) != list:
            raise Exception(f"invalid \"--dirs\" variable type: must be \"list\", but it's \"{type(self.options["--dirs"])}\"")

        for i in range(len(self.options["--dirs"])):
            dir:str = self.options["--dirs"][i]
            if not path.exists(dir) or not path.isdir(dir):
                raise Exception(f"Invalid directory path: {dir}")

            self.options["--dirs"][i] = path.abspath(dir)
            Log.Info(f"Included dir: {self.options['--dirs'][i]}")

        # Common dir to determinate where to place output dir
        if len(self.options["--files"]) == 0 and len(self.options["--dirs"]) == 0:
            # commonpath returns the file itself when there's exactly one path, so strip the filename manually
            self.commonPath = path.dirname(self.entryPoint)
        else:
            allPaths: list[str] = self.options["--files"]+self.options["--dirs"]+[self.entryPoint]
            self.commonPath = path.commonpath(allPaths) #Example of commonPath: /home/usr/python/pyguard/examples/complex-legacy/

        pathParts: list[str] = self.commonPath.split(path.sep)
        if self.commonPath == path.sep or len(pathParts) <= 2:
            Log.Warning(f"Computed common root \"{self.commonPath}\" is suspiciously shallow; the paths appear to come from unrelated trees", pause=True)

        # Output dir
        if type(self.options["--output"]) != str:
            raise Exception(f"invalid \"--output\" variable type: must be \"str\", but it's \"{type(self.options["--output"])}\"")
        if not self.options["--output"]:
            self.options["--output"] = "obfuscated"

        outputPath:str = path.join(self.commonPath, self.options["--output"])
        if path.exists(outputPath):
            Log.Warning(f"Output directory already exists: {outputPath}")

            response = ""

            while response != "y" and response != "n" and response != "ignored":
                response:str = Log.Question("Override directory? (y/n)").lower()

                match response:
                    case "ignored":
                        rmtree(outputPath)
                        Log.Info("Directory overridden")
                        break

                    case "y":
                        rmtree(outputPath)
                        Log.Success("Directory overridden")
                        break

                    case "n":
                        Log.Success("Directory skipped")
                        break

                    case _:
                        Log.Fail("Invalid response. Please enter 'y' or 'n'")

        Log.Info(f"Output dir: {outputPath}")
        Log.Custom("",end='\n')# Separator

    def ObfuscateFiles(self) -> None:
        # pyrefly: ignore [bad-argument-type] - all those were already checked in ValidateParams
        self.obfuscation = MainObfuscation(self.options["--hashdata"], self.options["--fernet"], self.options["--aes"], self.options["--chacha"], self.options["--salsa"], self.options["--base64"], self.options["--recursive"], self.options["--no-protect"], self.options["--enc-exec"])

        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--files"] can only be list[str]
        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                content:str = pyFile.read()
            if not content:
                Log.Warning(f"File {file} is empty")
                continue

            filepath, filename = path.split(file)
            content = RemoveComments(content)
            self.FollowImports(content)

            encBytes:bytes = self.obfuscation.Obfuscate(content)
            content = self.obfuscation.Wrap(encBytes)

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/
            # commonpath: /home/usr/python/pyguard/examples/complex-legacy/
            # result: .

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/dir/dir
            # commonpath: /home/usr/python/pyguard/examples/complex-legacy/
            # result: ./dir/dir

            self.SaveFile(filename, path.relpath(filepath, self.commonPath), content)

            #!!! TEMPORARY DISABLED CUZ FILE PATH HANDLING CHANGED !!!
            #self.obfuscation.ProtectFileModifications(self.options["--output"], path.join(filepath,filename))

        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--dirs"] can only be list[str]
        for dir in self.options["--dirs"]:
            for dirpath, dirnames, filenames in walk(dir):
                for filename in filenames:

                    if filename.endswith(".py"):
                        with open(path.join(dirpath,filename), "r", encoding="utf-8") as file:
                            content: str = file.read()
                        if not content:
                            Log.Warning(f"Empty file {filename} in dir {dirpath}")
                            continue

                        content = RemoveComments(content)
                        self.FollowImports(content)

                        encBytes:bytes = self.obfuscation.Obfuscate(content)
                        content = self.obfuscation.Wrap(encBytes)

                        #Same as above applies here
                        self.SaveFile(filename, path.relpath(dirpath, self.commonPath), content)

                        #!!! TEMPORARY DISABLED CUZ FILE PATH HANDLING CHANGED !!!
                        #self.obfuscation.ProtectFileModifications(self.options["--output"], path.join(filepath,filename))

            with open(self.entryPoint, "r", encoding="utf-8") as pyFile:
                content:str = pyFile.read()
            if not content:
                raise Exception(f"File {self.entryPoint} is empty")

            filepath, filename = path.split(self.entryPoint)
            content = RemoveComments(content)
            self.FollowImports(content)

            encBytes:bytes = self.obfuscation.Obfuscate(content)
            content = self.obfuscation.Wrap(encBytes)

            #Same as above applies here
            self.SaveFile(filename, path.relpath(filepath, self.commonPath), content)

            #!!! TEMPORARY DISABLED CUZ FILE PATH HANDLING CHANGED !!!
            #self.obfuscation.ProtectFileModifications(self.options["--output"], path.join(filepath,filename))

    def SaveFile(self, filename: str, relpath: str, content: str, entry:bool = False) -> None:
        imports = ""
        if entry:
            for module in self.imports:
                imports+=f"import {module}\n"
            content = imports + content

        # pyrefly: ignore [no-matching-overload] - already checked in ValidateParams, self.options["--output"] can only be str
        filepath = path.normpath(path.join(self.commonPath, self.options["--output"], relpath))
        # filepath: commonpath(/home/usr/python/pyguard/examples/complex-legacy/) + obfuscated + relpath(./dir/dir) => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/./dir/dir => normpath => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/dir/dir
        makedirs(filepath, exist_ok=True)

        with open(path.join(filepath,filename), "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"{filename} saved in {path.abspath(filepath)}")

    def FollowImports(self, content: str) -> None:
        if self.options["--follow-imports"]:
            modules:list[str] = GetImports(content)

            if not self.options["--no-protect"]:
                modules += ["hashlib", "os"]

            if self.options["--chacha"] or self.options["--salsa"]:
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
