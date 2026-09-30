from typing import override
from os import path, walk, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.legacyObfuscation import LegacyObfuscation
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
        try:
            self.ValidateParams()
        except TypeError as error:
            raise TypeError("Parameter validation error: internal error: " + str(error)) from error
        except ValueError as error:
            raise ValueError("Parameter validation error: " + str(error)) from error

        try:
            self.ObfuscateFiles()
        except Exception as error:
            raise Exception("Execution error: " + str(error)) from error

        Log.Success("Legacy obfuscation completed", bypassQuiet=True)

    def InitVars(self) -> None:
        self.projRoot:str

    @override
    def ValidateParams(self) -> None:
        if type(self.options["--loops"]) != int:
            raise TypeError(f"invalid \"--loops\" variable type: must be \"int\", but it's \"{type(self.options["--loops"])}\"")
        if self.options["--loops"] < 1:
            raise ValueError("Invalid --loops value")
        Log.Info(f"Loops amount: {self.options["--loops"]}")

        if type(self.options["--mode"]) != int:
            raise TypeError(f"invalid \"--mode\" variable type: must be \"int\", but it's \"{type(self.options["--mode"])}\"")
        if self.options["--mode"] < 1 or self.options["--mode"] > 4:
            raise ValueError("Invalid --mode value")
        Log.Info(f"Obfuscation mode: {self.options["--mode"]}")

        Log.Custom("",end='\n')# Separator

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
        if len(self.options["--files"]) == 1 and len(self.options["--dirs"]) == 0:
            # projRoot returns the file itself when there's exactly one path, so strip the filename manually
            self.projRoot = path.dirname(self.options["--files"][0])
        else:
            allPaths: list[str] = self.options["--files"]+self.options["--dirs"]
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
        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--files"] can only be list[str]
        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                content:str = pyFile.read()
            if not content:
                Log.Warning(f"File {file} is empty")
                continue

            content = RemoveComments(content)
            # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams self.options["--mode"] and self.options["--loops"] can only be int
            obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
            content = obfuscator.Encrypt(content)
            content = obfuscator.Wrap(content)

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/main.py
            # projRoot: /home/usr/python/pyguard/examples/complex-legacy/
            # relpath: main.py

            # filepath: /home/usr/python/pyguard/examples/complex-legacy/dir/dir/result.py
            # projRoot: /home/usr/python/pyguard/examples/complex-legacy/
            # relpath: dir/dir/result.py

            self.SaveFile(path.relpath(file, self.projRoot), content)# relpath -> path to file in project

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

                    # pyrefly: ignore [bad-argument-type] - already checked in ValidateParams self.options["--mode"] and self.options["--loops"] can only be int
                    obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
                    content = obfuscator.Encrypt(content)
                    content = obfuscator.Wrap(content)

                    #Same as above applies here
                    self.SaveFile(path.relpath(file, self.projRoot), content)# relpath -> path to file in project

    def SaveFile(self, relfilepath: str, content: str) -> None:
        # pyrefly: ignore [no-matching-overload] - already checked in ValidateParams, self.options["--output"] can only be str
        filepath = path.normpath(path.join(self.options["--output"], relfilepath))
        # filepath: projRoot(/home/usr/python/pyguard/examples/complex-legacy/) + obfuscated + relpath(./dir/dir) => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/./dir/dir => normpath => /home/usr/python/pyguard/examples/complex-legacy/obfuscated/dir/dir
        makedirs(path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"File {path.basename(filepath)} saved as {filepath}")
