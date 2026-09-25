from utils.logger import Log
from config import Command

class Help(Command):
    exclusiveOptions = []
    requiredOptions = []
    options = {}

    help = f'''
Usage:
  dotpyguard <command> [options]
Example:
  dotpyguard obfuscate --help

Commands:
  obfuscate         -> obfuscate code using advanced techniques.
  obfuscatelegacy   -> obfuscate code using legacy techniques.
  dependencies      -> command to work with dependencies.
  info              -> show general information about the program.
  help              -> show general help.

General Options:
  --help            -> show help for commands.
  --quiet           -> give less output.
  --log <path>      -> write all logs to a file.
  --no-color        -> suppress colored output.
  --no-input        -> disable prompting for input.'''

    def __init__(self, command: Command = None):
        if command == None:
            command = self
        Log.Custom(command.help)