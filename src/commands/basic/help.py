from utils.logger import Log
from config import Command

class Help(Command):
    exclusiveOptions: list[str | list[str]] = []
    requiredOptions: list[str | list[str]] = []
    options: dict[str , bool | int | str | list[str]] = {}

    help = f'''
Usage:
  pyguard <command> [options]
Example:
  pyguard obfuscate --help

Commands:
  obfuscate         -> encrypts/obfuscates and protects code using advanced techniques and methods
                       layered encryption, per-build identifier
                       randomization, an integrity manifest, runtime anti-analysis
                       controls, and compilation to a native extension module.
                       Protects for protecting code from static/dynamic analysis,
                       decompilation and reverse engineering.
  obfuscatelegacy   -> encrypts/obfuscates code using legacy method compression, byte reversal,
                       base64, and Fernet layers wrapped in an exec-based loader.
                       There are no integrity checks, no anti-analysis controls, and no compilation.
                       Best usage scenario is to prevent detection by antivirus.
                       Not suitable against a skilled attacker.
  dependencies      -> handles and works with dependencies
  info              -> shows general information about the program
  help              -> shows this message, the general help

General Options:
  --help            -> get help for commands
  --quiet           -> give less output
  --log <path>      -> duplicate all logs to a file
  --no-color        -> suppress colored output
  --no-input        -> disable prompting for input'''

    def __init__(self, command: Command | None = None) -> None:
        if command == None:
            Log.Custom(self.help, bypassQuiet=True)
        else:
            Log.Custom(command.help, bypassQuiet=True)
