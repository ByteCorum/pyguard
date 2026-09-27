from typing import override
from os import path, walk, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.obfuscation import LegacyObfuscation
from utils.langMgr import RemoveComments

class Obfuscatelegacy(Command):
    exclusiveOptions: list[str | list[str]] = []
    requiredOptions: list[str | list[str]] = ["--loops", "--mode", ["--files", "--dirs"]]
    options: dict[str , bool | int | str | list[str]] = {
        "--quiet": False,
        "--log": "",
        "--no-color": False,
        "--no-input": False,

        "--loops": 0,
        "--mode": 0,
        "--dirs": [],
        "--files": [],
        "--output": ""
    }

    help = f'''
Usage:
  pyguard obfuscatelegacy [options]
Example:
  pyguard obfuscatelegacy --loops 3 --mode 2 --file code.py

Notes:
  *                 -> required option
  text,text         -> to add more than one arg to option

Options:
  --help            -> show help for commands
  --quiet           -> give less output
  --log <path>      -> write all logs to a file
  --no-color        -> suppress colored output
  --no-input        -> disable prompting for input

  --loops <num>*    -> number of obfuscation loops
  --mode <num>*     -> obfuscation mode(1-4) as bigger number as better obfuscation but the output file is larger
  --dirs <path>*    -> obfuscate all files in dir(required files or/and dir)
  --files <path>*   -> files for obfuscation(required files or/and dir)
  --output <path>   -> output dir'''

    def __init__(self) -> None:
        Log.Info("Legacy obfuscation")

        self.InitVars()
        self.ValidateParams()
        self.ObfuscateFiles()

        Log.Success("Legacy obfuscation completed", bypassQuiet=True)

    def InitVars(self) -> None:
        self.commonPath:str

    @override
    def ValidateParams(self) -> None:
        if type(self.options["--loops"]) != int:
            raise Exception(f"invalid \"--loops\" variable type: must be \"int\", but it's \"{type(self.options["--loops"])}\"")
        if self.options["--loops"] < 1:
            raise Exception("Invalid --loops value")
        Log.Info(f"Loops amount: {self.options["--loops"]}")

        if type(self.options["--mode"]) != int:
            raise Exception(f"invalid \"--mode\" variable type: must be \"int\", but it's \"{type(self.options["--mode"])}\"")
        if self.options["--mode"] < 1 or self.options["--mode"] > 4:
            raise Exception("Invalid --mode value")
        Log.Info(f"Obfuscation mode: {self.options["--mode"]}")

        Log.Custom("",end='\n')# Separator

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
        if len(self.options["--files"]) == 1 and len(self.options["--dirs"]) == 0:
            # commonpath returns the file itself when there's exactly one path, so strip the filename manually
            self.commonPath = path.dirname(self.options["--files"][0])
        else:
            allPaths: list[str] = self.options["--files"]+self.options["--dirs"]
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
        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--files"] can only be list[str]
        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                content:str = pyFile.read()
            if not content:
                Log.Warning(f"File {file} is empty")
                continue

            filepath, filename = path.split(file)
            content = RemoveComments(content)

            # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams self.options["--mode"] and self.options["--loops"] can only be int
            obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
            content = obfuscator.Encrypt(content)
            content = obfuscator.Wrap(content)

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/
            # commonpath: /home/usr/python/pyguard/examples/complex-legacy/
            # result: .

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/dir/dir
            # commonpath: /home/usr/python/pyguard/examples/complex-legacy/
            # result: ./dir/dir

            self.SaveFile(filename, path.relpath(filepath, self.commonPath), content)

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

                        # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams self.options["--mode"] and self.options["--loops"] can only be int
                        obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
                        content = obfuscator.Encrypt(content)
                        content = obfuscator.Wrap(content)

                        #Same as above applies here
                        self.SaveFile(filename , path.relpath(dirpath, self.commonPath), content)

    def SaveFile(self, filename: str, relpath: str, content: str) -> None:
        # pyrefly: ignore [no-matching-overload] - already checked in ValidateParams, self.options["--output"] can only be str
        filepath = path.normpath(path.join(self.commonPath, self.options["--output"], relpath))
        # filepath: commonpath(/home/usr/python/pyguard/examples/complex-legacy/) + obfuscated + relpath(./dir/dir) => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/./dir/dir => normpath => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/dir/dir
        makedirs(filepath, exist_ok=True)

        with open(path.join(filepath,filename), "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"{filename} saved in {path.abspath(filepath)}")
