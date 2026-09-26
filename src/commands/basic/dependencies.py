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
        "--no-color ": False,
        "--no-input": False,

        "--show": False,
        "--install": False,
        "--uninstall": False,
        "--update": False,
    }

    help = f'''
Usage:
  pyguard dependencies [options]
Example:
  pyguard dependencies --quiet --no-input y --install

Note:
  `                 -> only one option from a group can be used.
  *                 -> required option.

Options:
  --help            -> show help for commands.
  --quiet           -> give less output.
  --log <path>      -> write all logs to a file.
  --no-color        -> suppress colored output.
  --no-input        -> disable prompting for input.

  --show*`          -> show all dependencies of the program.
  --install*`       -> install all dependencies of the program.
  --uninstall*`     -> uninstall all dependencies of the program.
  --update*`        -> update all dependencies of the program'''

    @staticmethod
    def __pip(args: list[str], dep: str) -> CompletedProcess[str]:
        command: list[str] = ["pip", *args]

        if Log.logFile:
            command += ["--log", Log.logFile]
        if Log.quiet:
            command.append("--quiet")
        if Log.noInput:
            command.append("--no-input")

        command.append(dep)
        return run(command, capture_output=True, text=True)

    def __init__(self) -> None:
        if self.options["--show"]:
            string = ""
            for dep in DEPENDENCIES:
                string += f"\n  {dep}"
            Log.Custom(f"Project's dependencies:{string}")

        if self.options["--install"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["install"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" installed")
                else:
                    Log.Fail(f"Failed to install {dep}: {result.stderr.strip()}")

        if self.options["--uninstall"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["uninstall", "-y"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" uninstalled")
                else:
                    Log.Fail(f"Failed to uninstall {dep}: {result.stderr.strip()}")

        if self.options["--update"]:
            for dep in DEPENDENCIES:
                result: CompletedProcess[str] = self.__pip(["install", "--upgrade"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" updated")
                else:
                    Log.Fail(f"Failed to update {dep}: {result.stderr.strip()}")
