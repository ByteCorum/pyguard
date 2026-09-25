from os import system
from utils.logger import Log
from config import Command

class Dependencies(Command):
    exclusiveOptions = [["--show", "--install", "--uninstall", "--update"]]
    requiredOptions = [["--show", "--install", "--uninstall", "--update"]]

    options = {
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
  dotpyguard dependencies [options]
Example:
  dotpyguard dependencies --quiet --no-input y --install

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

    def __init__(self):
        dependencies = ["cryptography", "pycryptodome", "cython", "nuitka", "colorama", "setuptools"]

        if self.options["--show"]:
            string = ""
            for dep in dependencies:
                string+=f"\n  {dep}"
            Log.Custom(f"Project's dependencies:{string}")

        if self.options["--install"]:
            for dep in dependencies:
                system(f"pip install {f" --log {Log.logFile}" if Log.logFile else ""}{ "--quiet" if Log.quiet else ""}{ "--no-input" if Log.noInput else ""} {dep}")
                Log.Success("Dependencies installed")

        if self.options["--uninstall"]:
            for dep in dependencies:
                system(f"pip uninstall {f" --log {Log.logFile}" if Log.logFile else ""}{ "--quiet" if Log.quiet else ""}{ "--no-input" if Log.noInput else ""} {dep}")
                Log.Success("Dependencies uninstalled")

        if self.options["--update"]:
            for dep in dependencies:
                system(f"pip install --upgrade {f" --log {Log.logFile}" if Log.logFile else ""}{ "--quiet" if Log.quiet else ""}{ "--no-input" if Log.noInput else ""} {dep}")
                Log.Success("Dependencies updated")