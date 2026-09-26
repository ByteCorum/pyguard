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
  `                 -> only one option from a group can be used.
  *                 -> required option.

Options:
  --help            -> show help for commands.
  --log <path>      -> write all logs to a file.
  --no-color        -> suppress colored output.

  --all*`           -> show all information about the program.
  --version*`       -> show version of the program.
  --url*`           -> show URL of program's github repo.
  --description*`   -> show description of the program.'''

    def __init__(self) -> None:
        if self.options["--all"]:
            Log.Custom(f"{NAME} version {VERSION}\nby {AUTHOR}\n{DESCRIPTION}\nRepo: {URL}", bypassQuiet=True)

        elif self.options["--version"]:
            Log.Custom(f"{NAME} version {VERSION}", bypassQuiet=True)

        elif self.options["--url"]:
            Log.Custom(f"Repo: {URL}", bypassQuiet=True)

        elif self.options["--description"]:
            Log.Custom(f"{DESCRIPTION}", bypassQuiet=True)
