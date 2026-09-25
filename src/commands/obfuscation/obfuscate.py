from os import path, sep, walk, getcwd, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.langMgr import RemoveComments, GetImports
from utils.obfuscation import MainObfuscation

class Obfuscate(Command):
    exclusiveOptions = []
    requiredOptions = ["entrypoint", ["--hashdata", "--fernet", "--aes", "--chacha", "--salsa" "--base64", "--recursive"]]
    options = {
        "--quiet": False,
        "--log": "",
        "--no-color ": False,
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
  dotpyguard obfuscate [options] main.py
Example:
  dotpyguard obfuscate --hashdata --aes --follow-imports main.py

Notes:
  text,text         -> to add more than one arg to option.
  main.py           -> the entry point of your program.

Options:
  --help            -> show help for commands.
  --quiet           -> give less output.
  --log <path>      -> write all logs to a file.
  --no-color        -> suppress colored output.
  --no-input        -> disable prompting for input.

  --hashdata        -> convert all strings and var names into hash.
  --fernet          -> obfuscation and encryption using fernet.
  --aes             -> obfuscation and encryption using aes256.
  --chacha          -> obfuscation and encryption using chacha20.
  --salsa           -> obfuscation and encryption using salsa20.
  --base64          -> obfuscation and encryption using base64.
  --recursive <num> -> not strong but good if u need to hide ur prog from AVs.
  --no-protect      -> disable file modification protection.
  --enc-exec        -> obfuscate executor via legacy encryption method.
  --dirs <path>     -> obfuscate all files in dir.
  --files <path>    -> files for obfuscation.
  --output <path>   -> output dir.
  --follow-imports  -> add all imports to the protected script.'''

    def __init__(self):
        self.InitVars()
        self.CheckOptions()
        self.ObfuscateFiles()
        self.obfuscation.CreateExecutor(self.options["--output"])
        Log.Success("Obfuscation compleated")

    def InitVars(self):
        self.workingDir = getcwd()
        self.imports = []

    def CheckOptions(self):
        Log.Info("Obfuscation")
        if self.options["--recursive"] < 0:
            raise Exception("Invalid --recursive value.")

        if not self.options["--output"]:
            self.options["--output"] = "obfuscated"

        if path.exists(self.options["--output"]):
            Log.Warning(f"Output directory already exists: \"{self.options['--output']}\".")
            responce = ""
            while responce != "y" or responce != "n" or responce != "ignore":
                responce = Log.Question("Override directory? (y/n)").lower()

                match responce:
                    case "ignore":
                        rmtree(self.options["--output"])
                        Log.Info("Directory overridden.")
                        break
                    case "y":
                        rmtree(self.options["--output"])
                        Log.Success("Directory overridden.")
                        break
                    case "n":
                        Log.Success("Directory skipped.")
                        break
                    case _:
                        Log.Fail("Invalid response. Please enter 'y' or 'n'.")
            print()

        self.entryPoint = self.options["entrypoint"]
        if not path.exists(self.entryPoint) or not path.isfile(self.entryPoint) or not self.entryPoint.endswith(".py"):
            raise Exception(f"Invalid entrypoint path: \"{self.entryPoint}\".")
        if path.isabs(self.entryPoint):
            raise Exception(f"Abs path is unsupported: \"{self.entryPoint}\"")

        for file in self.options["--files"]:
            if not path.exists(file) or not path.isfile(file) or not file.endswith(".py"):
                raise Exception(f"Invalid file path: \"{file}\".")
            if path.isabs(file):
                raise Exception(f"Abs path is unsupported: \"{file}\"")

        for dir in self.options["--dirs"]:
            if not path.exists(dir) or not path.isdir(dir):
                raise Exception(f"Invalid directory path: \"{dir}\".")
            if path.isabs(dir):
                raise Exception(f"Abs path is unsupported: \"{dir}\"")

        Log.Info(f"Entrypoint file: {self.entryPoint}")
        if self.options["--files"]:
            Log.Info(f"Included files: {self.options["--files"]}")
        if self.options["--dirs"]:
            Log.Info(f"Included dirs: {self.options["--dirs"]}")

        methods = f"{"hashdata, " if self.options["--hashdata"] else ""}{"fernet, " if self.options["--fernet"] else ""}{"aes, " if self.options["--aes"] else ""}{"chacha20, " if self.options["--chacha"] else ""}{"salsa20, " if self.options["--salsa"] else ""}{"base64, " if self.options["--base64"] else ""}{f"recursive<{self.options["--recursive"]}>, " if self.options["--recursive"]>0 else ""}"[:-2]
        if methods:
            Log.Info(f"Obfuscation methods: {methods}")

        options = f"{"follow-imports, " if self.options["--follow-imports"] else ""}{"no-protect, " if self.options["--no-protect"] else ""}"[:-2]
        if options:
            Log.Info(f"Additional options: {options}")
        Log.Info(f"output dir: {self.options["--output"]}\n")

    def ObfuscateFiles(self):
        self.obfuscation = MainObfuscation(self.options["--hashdata"],
                                           self.options["--fernet"],
                                           self.options["--aes"],
                                           self.options["--chacha"],
                                           self.options["--salsa"],
                                           self.options["--base64"],
                                           self.options["--recursive"],
                                           self.options["--no-protect"],
                                           self.options["--enc-exec"])

        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                context = pyFile.read()
            if not context:
                Log.Warning(f"File {file} is empty")
                continue

            filepath, filename = path.split(file)
            if filepath:
                filepath = path.relpath(filepath, self.workingDir)

            context = RemoveComments(context)
            self.FollowImports(context)

            context = self.obfuscation.Obfuscate(context)
            context = self.obfuscation.Wrap(context)

            self.SaveFile(filename, filepath, context)
            self.obfuscation.ProtectFile(self.options["--output"], filepath+sep+filename)

        for dir in self.options["--dirs"]:
            for dirpath, dirnames, filenames in walk(dir):
                for filename in filenames:

                    if filename.endswith(".py"):
                        with open(dirpath+sep+filename, "r", encoding="utf-8") as file:
                            context = file.read()
                        if not context:
                            Log.Warning(f"Empty file {filename} in dir {dirpath}")
                            continue

                        dirpath = path.relpath(dirpath, self.workingDir)

                        context = RemoveComments(context)
                        self.FollowImports(context)

                        context = self.obfuscation.Obfuscate(context)
                        context = self.obfuscation.Wrap(context)

                        self.SaveFile(filename , dirpath, context)
                        self.obfuscation.ProtectFile(self.options["--output"], dirpath+sep+filename)

        with open(self.entryPoint, "r", encoding="utf-8") as pyFile:
            context = pyFile.read()
        if not context:
            Log.Error(f"Entrypoint file {self.entryPoint} is empty")

        filepath, filename = path.split(self.entryPoint)
        if filepath:
            filepath = path.relpath(filepath, self.workingDir)

        context = RemoveComments(context)
        self.FollowImports(context)

        context = self.obfuscation.Obfuscate(context)
        context = self.obfuscation.Wrap(context)

        self.SaveFile(filename, filepath, context, entrypoint = True)
        self.obfuscation.ProtectFile(self.options["--output"], filepath+sep+filename)

    def SaveFile(self, filename, filepath, content, entrypoint = False):
        imports = ""
        if entrypoint:
            for module in self.imports:
                imports+=f"import {module}\n"

        filepath = self.options["--output"]+sep+filepath
        makedirs(filepath, exist_ok=True)

        with open(filepath+sep+filename, "w", encoding="utf-8") as file:
            if entrypoint:
                file.write(imports)
            file.write(content)

        Log.Info(f"{filename} saved in {filepath[:-1]}")

    def FollowImports(self, content):
        if self.options["--follow-imports"]:
            modules = GetImports(content)

            if not self.options["--no-protect"]:
                modules.append("hashlib")
                modules.append("os")

            if self.options["--chacha"] or self.options["--salsa"]:
                modules.append("Crypto.Cipher")

            if self.options["--aes"]:
                modules.append("cryptography.hazmat.primitives.ciphers.aead")

            if self.options["--fernet"]:
                modules.append("cryptography.fernet")

            modules.append("sys")
            modules.append("base64")
            modules.append("zlib")

            for module in modules:
                if not module in self.imports:
                    self.imports.append(module)
