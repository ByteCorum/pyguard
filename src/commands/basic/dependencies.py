from multiprocessing.reduction import Type
from typing import override
from subprocess import CompletedProcess
from subprocess import run
from utils.logger import Log
from config import Command, DEPENDENCIES

class Dependencies(Command):
    exclusiveOptions: list[str | list[str]] = [["--show", "--install", "--uninstall", "--update"]]
    requiredOptions: list[str | list[str]] = [["--show", "--install", "--uninstall", "--update"]]

    options: dict[str , bool | int | str | list[str]] = {
        "--quiet": False,
        "--log": "",
        "--no-color": False,

        "--show": False,
        "--install": False,
        "--uninstall": False,
        "--update": False,
    }

    help = f'''
Usage:
  pyguard dependencies [options]
Example:
  pyguard dependencies --quiet --no-input --install

Options:
  --help            -> get help for commands
  --quiet           -> give less output
  --log <path>      -> duplicate all logs to a file
  --no-color        -> suppress colored output
  --no-input        -> disable prompting for input

  --show            -> show dependencies of the program
  --install         -> install dependencies of the program
  --uninstall       -> uninstall dependencies of the program
  --update          -> update dependencies of the program

Note:
  Mutual exclusive required options:
    --show, --install, --uninstall, --update
 '''

    @staticmethod
    def __pip(args: list[str], dep: str) -> CompletedProcess[str]:
        command: list[str] = ["pip", *args]

        if Log.logFile:
            command += ["--log", Log.logFile]
        if Log.quiet:
            command += ["--quiet", "--quiet"]
        if Log.noInput:
            command.append("--no-input")

        command.append(dep)
        return run(command, capture_output=True, text=True)

    @staticmethod
    def __logPip(result: CompletedProcess[str]) -> None:
        if result.stdout.strip():
            Log.Custom(result.stdout.strip())
        if result.stderr.strip():
            Log.Custom(result.stderr.strip(), bypassQuiet=True)

    def __init__(self) -> None:
        try:
            self.ValidateParams()
        except TypeError as error:
            raise TypeError("Parameter validation error: " + str(error)) from error
        try:
            self.RunOption()
        except Exception as error:
            raise TypeError("Execution error: " + str(error)) from error

    @override
    def ValidateParams(self) -> None:
        if type(self.options["--show"]) != bool:
            raise TypeError(f"internal error: invalid \"--show\" variable type: must be \"bool\", but it's \"{type(self.options["--show"])}\"")
        if type(self.options["--install"]) != bool:
            raise TypeError(f"internal error: invalid \"--install\" variable type: must be \"bool\", but it's \"{type(self.options["--install"])}\"")
        if type(self.options["--uninstall"]) != bool:
            raise TypeError(f"internal error: invalid \"--uninstall\" variable type: must be \"bool\", but it's \"{type(self.options["--uninstall"])}\"")
        if type(self.options["--update"]) != bool:
            raise TypeError(f"internal error: invalid \"--update\" variable type: must be \"bool\", but it's \"{type(self.options["--update"])}\"")

    def RunOption(self) -> None:
        if self.options["--show"]:
            string = ""
            for dep in DEPENDENCIES:
                string += f"\n  {dep}"
            Log.Custom(f"Project's dependencies:{string}")

        if self.options["--install"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["install"], dep)
                self.__logPip(result)

                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" installed")
                else:
                    Log.Fail(f"Failed to install {dep}: {result.stderr.strip()}")

        if self.options["--uninstall"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["uninstall", "-y"], dep)
                self.__logPip(result)

                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" uninstalled")
                else:
                    Log.Fail(f"Failed to uninstall {dep}: {result.stderr.strip()}")

        if self.options["--update"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["install", "--upgrade"], dep)
                self.__logPip(result)

                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" updated")
                else:
                    Log.Fail(f"Failed to update {dep}: {result.stderr.strip()}")
