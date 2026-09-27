from os import path, sep, walk, getcwd, makedirs
from shutil import rmtree
from utils.logger import Log
from config import Command
from utils.obfuscation import LegacyObfuscation
from utils.langMgr import RemoveComments

# !!! TODO refactor this file

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

    def __init__(self) -> None:
        self.cwd:str = getcwd()

        self.CheckOptions()

        # pyrefly: ignore [no-matching-overload, unsupported-operation]
        self.commonPath:str = path.commonpath(self.options["--files"]+self.options["--dirs"])

        pathParts: list[str] = self.commonPath.split(path.sep)
        if self.commonPath == path.sep or len(pathParts) <= 2:
            Log.Warning(f"Computed common root \"{self.commonPath}\" is suspiciously shallow; the paths appear to come from unrelated trees", pause=True)

        self.ObfuscateFiles()

        Log.Success("Legacy obfuscation completed", bypassQuiet=True)

    def CheckOptions(self) -> None:
        Log.Info("Legacy obfuscation")

        # pyrefly: ignore [unsupported-operation] - if --loops is not an int program must loudly fail
        if self.options["--loops"] < 1:
            raise Exception("Invalid --loops value")

        # pyrefly: ignore [unsupported-operation] - if --mode is not an int program must loudly fail
        if self.options["--mode"] < 1 or self.options["--mode"] > 4:
            raise Exception("Invalid --mode value")

        if not self.options["--output"]:
            self.options["--output"] = "obfuscated"

        # pyrefly: ignore [no-matching-overload] - if --output is not a string program must loudly fail
        if path.exists(path.join(self.cwd,self.options["--output"])):
            Log.Warning(f"Output directory already exists: \"{self.options['--output']}\"")
            response = ""
            while response != "y" or response != "n" or response != "ignored":
                response:str = Log.Question("Override directory? (y/n)").lower()

                match response:
                    case "ignored":
                        # pyrefly: ignore [bad-argument-type] - if --output is not a string program must loudly fail
                        rmtree(self.options["--output"])
                        Log.Info("Directory overridden\n")
                        break

                    case "y":
                        # pyrefly: ignore [bad-argument-type] - if --output is not a string program must loudly fail
                        rmtree(self.options["--output"])
                        Log.Success("Directory overridden\n")
                        break

                    case "n":
                        Log.Success("Directory skipped\n")
                        break

                    case _:
                        Log.Fail("Invalid response. Please enter 'y' or 'n'\n")

        # pyrefly: ignore [bad-argument-type] - if --files is not a list program must loudly fail
        for i in range (len(self.options["--files"])):
            # pyrefly: ignore [bad-index] - if --files is not a list program must loudly fail
            file:str = self.options["--files"][i]
            if not path.exists(file) or not path.isfile(file) or not file.endswith(".py"):
                raise Exception(f"Invalid file path: \"{file}\"")

            # pyrefly: ignore [unsupported-operation]
            self.options["--files"][i] = path.abspath(file)
            # pyrefly: ignore [bad-index]
            Log.Info(f"Included file: {self.options["--files"][i]}")

        # pyrefly: ignore [bad-argument-type] - if --dirs is not a list program must loudly fail
        for i in range(len(self.options["--dirs"])):
            # pyrefly: ignore [bad-index] - if --dirs is not a list program must loudly fail
            dir:str = self.options["--dirs"][i]

            if not path.exists(dir) or not path.isdir(dir):
                raise Exception(f"Invalid directory path: \"{dir}\"")

            # pyrefly: ignore [unsupported-operation]
            self.options["--dirs"][i] = path.abspath(dir)
            # pyrefly: ignore [bad-index]
            Log.Info(f"Included dir: {self.options['--dirs'][i]}")

        Log.Info(f"Loops amount: {self.options["--loops"]}")
        Log.Info(f"Obfuscation mode: {self.options["--mode"]}")
        Log.Info(f"Output dir: {self.options["--output"]}\n")

    def ObfuscateFiles(self) -> None:
        # pyrefly: ignore [not-iterable] - if --files is not a list program must loudly fail
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

            self.SaveFile(filename, path.relpath(filepath, self.commonPath), context)

        # pyrefly: ignore [not-iterable] - if --dirs is not a list program must loudly fail
        for dir in self.options["--dirs"]:
            for dirpath, dirnames, filenames in walk(dir):
                for filename in filenames:

                    if filename.endswith(".py"):
                        with open(dirpath+sep+filename, "r", encoding="utf-8") as file:
                            context = file.read()
                        if not context:
                            Log.Warning(f"Empty file {filename} in dir {dirpath}")
                            continue

                        context = RemoveComments(context)

                        obfuscator = LegacyObfuscation(self.options["--mode"], self.options["--loops"], LegacyObfuscation.GenSeperator())
                        context = obfuscator.Encrypt(context)
                        context = obfuscator.Wrap(context)

                        self.SaveFile(filename , path.relpath(dirpath, self.commonPath), context)

    def SaveFile(self, filename: str, filepath: str, content: str) -> None:
        # pyrefly: ignore [no-matching-overload] - if --output is not a string program must loudly fail
        filepath = path.normpath(path.join(self.cwd, self.options["--output"], filepath))
        makedirs(filepath, exist_ok=True)

        with open(filepath+sep+filename, "w", encoding="utf-8") as file:
            file.write(content)

        Log.Info(f"{filename} saved in {filepath}")
