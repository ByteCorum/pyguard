from typing import override
from os import path, walk, getcwd, makedirs
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

        self.SetGlobals()
        self.ValidateParams()
        self.ObfuscateFiles()

        Log.Success("Legacy obfuscation completed", bypassQuiet=True)

    def SetGlobals(self) -> None:
        self.cwd:str = getcwd()
        self.commonPath:str = "."

    @override
    def ValidateParams(self) -> None:
        if type(self.options["--loops"]) != int:
            raise Exception(f"invalid \"--loops\" variable type: must be \"int\", but it's \"{type(self.options["--loops"])}\"")
        if self.options["--loops"] < 1:
            raise Exception("Invalid --loops value")

        if type(self.options["--mode"]) != int:
            raise Exception(f"invalid \"--mode\" variable type: must be \"int\", but it's \"{type(self.options["--mode"])}\"")
        if self.options["--mode"] < 1 or self.options["--mode"] > 4:
            raise Exception("Invalid --mode value")

        if type(self.options["--output"]) != str:
            raise Exception(f"invalid \"--output\" variable type: must be \"str\", but it's \"{type(self.options["--output"])}\"")
        if not self.options["--output"]:
            self.options["--output"] = "obfuscated"

        outputPath:str = path.join(self.cwd, self.options["--output"])
        if path.exists(outputPath):
            Log.Warning(f"Output directory already exists: \"{outputPath}\"")

            response = ""
            while response != "y" or response != "n" or response != "ignored":
                response:str = Log.Question("Override directory? (y/n)").lower()

                match response:
                    case "ignored":
                        rmtree(outputPath)
                        Log.Info("Directory overridden\n")
                        break

                    case "y":
                        rmtree(outputPath)
                        Log.Success("Directory overridden\n")
                        break

                    case "n":
                        Log.Success("Directory skipped\n")
                        break

                    case _:
                        # This should never happen
                        Log.Fail("Invalid response. Please enter 'y' or 'n'\n")

        if type(self.options["--files"]) != list[str]:
            raise Exception(f"invalid \"--files\" variable type: must be \"list[str]\", but it's \"{type(self.options["--files"])}\"")

        for i in range (len(self.options["--files"])):
            file:str = self.options["--files"][i]
            if not path.exists(file) or not path.isfile(file) or not file.endswith(".py"):
                raise Exception(f"Invalid file path: \"{file}\"")

            self.options["--files"][i] = path.abspath(file)
            Log.Info(f"Included file: {self.options["--files"][i]}")

        if type(self.options["--dirs"]) != list[str]:
            raise Exception(f"invalid \"--dirs\" variable type: must be \"list[str]\", but it's \"{type(self.options["--dirs"])}\"")

        for i in range(len(self.options["--dirs"])):
            dir:str = self.options["--dirs"][i]
            if not path.exists(dir) or not path.isdir(dir):
                raise Exception(f"Invalid directory path: \"{dir}\"")

            self.options["--dirs"][i] = path.abspath(dir)
            Log.Info(f"Included dir: {self.options['--dirs'][i]}")

        self.commonPath = path.commonpath(self.options["--files"]+self.options["--dirs"])

        pathParts: list[str] = self.commonPath.split(path.sep)
        if self.commonPath == path.sep or len(pathParts) <= 2:
            Log.Warning(f"Computed common root \"{self.commonPath}\" is suspiciously shallow; the paths appear to come from unrelated trees", pause=True)

        Log.Info(f"Loops amount: {self.options["--loops"]}")
        Log.Info(f"Obfuscation mode: {self.options["--mode"]}")
        Log.Info(f"Output dir: {self.options["--output"]}\n")

    def ObfuscateFiles(self) -> None:
        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--files"] can only be list[str]
        for file in self.options["--files"]:
            with open(file, "r", encoding="utf-8") as pyFile:
                context:str = pyFile.read()
            if not context:
                Log.Warning(f"File {file} is empty")
                continue

            filepath, filename = path.split(file)
            context = RemoveComments(context)

            obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
            context = obfuscator.Encrypt(context)
            context = obfuscator.Wrap(context)

            self.SaveFile(filename, filepath.replace(self.commonPath, ""), context)

        # pyrefly: ignore [not-iterable] - already checked in ValidateParams, self.options["--dirs"] can only be list[str]
        for dir in self.options["--dirs"]:
            for dirpath, dirnames, filenames in walk(dir):
                for filename in filenames:

                    if filename.endswith(".py"):
                        with open(path.join(dirpath,filename), "r", encoding="utf-8") as file:
                            context = file.read()
                        if not context:
                            Log.Warning(f"Empty file {filename} in dir {dirpath}")
                            continue

                        context = RemoveComments(context)

                        obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
                        context = obfuscator.Encrypt(context)
                        context = obfuscator.Wrap(context)

                        self.SaveFile(filename , dirpath.replace(self.commonPath, ""), context)

    def SaveFile(self, filename: str, filepath: str, content: str) -> None:
        # pyrefly: ignore [no-matching-overload] - already checked in ValidateParams, self.options["--output"] can only be str
        filepath = path.normpath(path.join(self.cwd, self.options["--output"], filepath))
        makedirs(filepath, exist_ok=True)

        with open(path.join(filepath+filename), "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"{filename} saved in {filepath}")
