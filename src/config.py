from abc import ABC

NAME = ".PyGuard"
AUTHOR = "ByteCorum"
URL = "https://github.com/ByteCorum/.PyGuard"
VERSION = "3.1.0.0"
DESCRIPTION = "Tool/Library for Python used to obfuscate and protect your code in static and runtime from decompilation, reverse debug, etc. Also, can prevent detection by antiviruses."

class Command(ABC):
    exclusiveOptions: list
    requiredOptions: list
    options: dict
    help: str

# class Name_of_the_command(Command): #note: only first letter should be capital
#     def __init__(self): #command handler that will be called when the command is executed
#         pass
#
#     #May be left not initialized if your command has no options#
#     exclusiveOptions = [["--install","--uninstall"], ["--up","--down"]] #groups of options that can't be used together
#     requiredOptions = ["entrypoint", [""]] #options and groups(any option from a group is required) that are required
#
#     options = { #all the options that your command has. note: don't write help here, it's hendeled elsewhere
#         #General Options
#         "--quiet": False,
#         "--log": "",
#         "--no-color ": False,
#         "--no-input": False,
#
#         #Your Options
#         "--option1": False,
#         "entrypoint": "" #only 1 fixed option name used to store program entrypoint file path
#     }
#
#     #Should be always initialized#
#     help = f'''I\'ll help u''' #help message for the command
#