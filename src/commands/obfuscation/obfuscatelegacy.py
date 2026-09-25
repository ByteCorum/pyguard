from os import path, sep, walk, getcwd, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.obfuscation import LegacyObfuscation
from utils.langMgr import RemoveComments

class Obfuscatelegacy(Command):
    exclusiveOptions = []
    requiredOptions = ["--loops", "--mode", ["--files", "--dirs"]]
    options = {
        "--quiet": False,
        "--log": "",
        "--no-color ": False,
        "--no-input": False,

        "--loops": 0,
        "--mode": 0,
        "--dirs": [],
        "--files": [],
        "--output": ""
    }

    help = f'''
Usage:
  dotpyguard obfuscatelegacy [options]
Example:
  dotpyguard obfuscatelegacy --loops 3 --mode 2 --file code.py

Notes:
  *                 -> required option.
  text,text         -> to add more than one arg to option.

Options:
  --help            -> show help for commands.
  --quiet           -> give less output.
  --log <path>      -> write all logs to a file.
  --no-color        -> suppress colored output.
  --no-input        -> disable prompting for input.

  --loops <num>*    -> number of obfuscation loops.
  --mode <num>*     -> obfuscation mode(1-4) as bigger number as better obfuscation but the output file is larger.
  --dirs <path>*    -> obfuscate all files in dir(required files or/and dir).
  --files <path>*   -> files for obfuscation(required files or/and dir).
  --output <path>   -> output dir.'''

    def __init__(self):
        self.InitVars()
        self.CheckOptions()
        self.ObfuscateFiles()
        Log.Success("Legacy obfuscation compleated")

    def InitVars(self):
        self.workingDir = getcwd()

    def CheckOptions(self):
        Log.Info("Legacy obfuscation.")

        if self.options["--loops"] < 1:
            raise Exception("Invalid --loops value.")
        if self.options["--mode"] < 1 or self.options["--mode"] > 4:
            raise Exception("Invalid --mode value.")

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

        if self.options["--files"]:
            Log.Info(f"Included files: {self.options["--files"]}")
        if self.options["--dirs"]:
            Log.Info(f"Included dirs: {self.options["--dirs"]}")

        Log.Info(f"loops amount: {self.options["--loops"]}")
        Log.Info(f"obfuscation mode: {self.options["--mode"]}")
        Log.Info(f"output dir: {self.options["--output"]}\n")

    def ObfuscateFiles(self):
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

            obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
            context = obfuscator.Encrypt(context)
            context = obfuscator.Wrap(context)

            self.SaveFile(filename, filepath, context)

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

                        obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
                        context = obfuscator.Encrypt(context)
                        context = obfuscator.Wrap(context)

                        self.SaveFile(filename , dirpath, context)

    def SaveFile(self, filename, filepath, content):
        filepath = self.options["--output"]+sep+filepath
        makedirs(filepath, exist_ok=True)

        with open(filepath+sep+filename, "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"{filename} saved in {filepath[:-1]}")