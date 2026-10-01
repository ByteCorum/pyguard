from dataclasses import dataclass
from typing import override
from subprocess import Popen, PIPE, CompletedProcess
from threading import Thread
from typing import IO
from utils.logger import Log
from config import Command, DEPENDENCIES

@dataclass
class PipResult:
    returncode: int
    stdout: str
    stderr: str

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
    def __pip(args: list[str], dep: str) -> PipResult:
        command: list[str] = ["pip", *args]

        if Log.logFile:
            command += ["--log", Log.logFile]
        if Log.quiet:
            command += ["--quiet", "--quiet"]
        if Log.noInput:
            command.append("--no-input")

        command += ["--progress-bar", "off", dep]

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        with Popen(command, stdout=PIPE, stderr=PIPE, text=True) as process:
            assert process.stdout is not None and process.stderr is not None

            def drain(stream: IO[str], sink: list[str], bypassQuiet: bool) -> None:
                for line in stream:
                    line:str = line.rstrip()
                    sink.append(line)
                    if line:
                        Log.Custom(line, bypassQuiet=bypassQuiet)

            readers: list[Thread] = [
                Thread(target=drain, args=(process.stdout, stdout_lines, False)),
                Thread(target=drain, args=(process.stderr, stderr_lines, True)),
            ]
            for reader in readers:
                reader.start()
            for reader in readers:
                reader.join()

            returncode: int = process.wait()

        return PipResult(returncode, "\n".join(stdout_lines), "\n".join(stderr_lines))

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
                result: PipResult = self.__pip(["install"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" installed")
                else:
                    Log.Fail(f"Failed to install {dep}: {result.stderr.strip()}")

        if self.options["--uninstall"]:
            for dep in DEPENDENCIES:
                result: PipResult = self.__pip(["uninstall", "-y"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" uninstalled")
                else:
                    Log.Fail(f"Failed to uninstall {dep}: {result.stderr.strip()}")

        if self.options["--update"]:
            for dep in DEPENDENCIES:
                result: PipResult = self.__pip(["install", "--upgrade"], dep)
                if result.returncode == 0:
                    Log.Success(f"Dependency \"{dep}\" updated")
                else:
                    Log.Fail(f"Failed to update {dep}: {result.stderr.strip()}")
