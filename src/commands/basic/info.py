from typing import override
from utils.logger import Log
from config import Command, NAME, VERSION, AUTHOR, URL, DESCRIPTION

class Info(Command):
    exclusiveOptions: list[str | list[str]] = [["--all", "--version", "--url", "--description"]]
    requiredOptions: list[str | list[str]] = [["--all", "--version", "--url", "--description"]]

    options: dict[str , bool | int | str | list[str]] = {
        "--log": "",
        "--no-color": False,

        "--all": False,
        "--version": False,
        "--url": False,
        "--description": False,
    }

    help = f'''
Usage:
  pyguard info [options]
Example:
  pyguard info --all

Note:
  `                 -> only one option from a group can be used
  *                 -> required option

Options:
  --help            -> show help for commands
  --log <path>      -> write all logs to a file
  --no-color        -> suppress colored output

  --all*`           -> show all information about the program
  --version*`       -> show version of the program
  --url*`           -> show URL of program's github repo
  --description*`   -> show description of the program'''

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
        if type(self.options["--all"]) != bool:
            raise TypeError(f"internal error: invalid \"--all\" variable type: must be \"bool\", but it's \"{type(self.options["--all"])}\"")
        if type(self.options["--version"]) != bool:
            raise TypeError(f"internal error: invalid \"--version\" variable type: must be \"bool\", but it's \"{type(self.options["--version"])}\"")
        if type(self.options["--url"]) != bool:
            raise TypeError(f"internal error: invalid \"--url\" variable type: must be \"bool\", but it's \"{type(self.options["--url"])}\"")
        if type(self.options["--description"]) != bool:
            raise TypeError(f"internal error: invalid \"--description\" variable type: must be \"bool\", but it's \"{type(self.options["--description"])}\"")

    def RunOption(self) -> None:
        if self.options["--all"]:
            Log.Custom(f"{NAME} version {VERSION}\nby {AUTHOR}\n{DESCRIPTION}\nRepo: {URL}", bypassQuiet=True)

        elif self.options["--version"]:
            Log.Custom(f"{NAME} version {VERSION}", bypassQuiet=True)

        elif self.options["--url"]:
            Log.Custom(f"Repo: {URL}", bypassQuiet=True)

        elif self.options["--description"]:
            Log.Custom(f"{DESCRIPTION}", bypassQuiet=True)
