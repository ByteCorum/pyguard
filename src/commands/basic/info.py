from utils.logger import Log, Fore
from config import Command, NAME, VERSION, AUTHOR, URL, DESCRIPTION

class Info(Command):
    exclusiveOptions = [["--all", "--version", "--url", "--description"]]
    requiredOptions = [["--all", "--version", "--url", "--description"]]

    options = {
        "--log": "",
        "--no-color": False,

        "--all": False,
        "--version": False,
        "--url": False,
        "--description": False,
    }

    help = f'''
Usage:
  dotpyguard info [options]
Example:
  dotpyguard info --all

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

    def __init__(self):
        if self.options["--all"]:
            Log.Custom(f"{NAME} version {VERSION}\nby {AUTHOR}\n{DESCRIPTION}\nRepo: {Fore.BLUE if Log.colored else ""}{URL}{Fore.RESET}")

        elif self.options["--version"]:
            Log.Custom(f"{NAME} version {VERSION}")

        elif self.options["--url"]:
            Log.Custom(f"Repo: {Fore.BLUE if Log.colored else ""}{URL}{Fore.RESET}")

        elif self.options["--description"]:
            Log.Custom(f"{DESCRIPTION}")