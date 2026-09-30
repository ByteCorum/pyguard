from abc import ABC
from os import path

NAME:str  = "PyGuard"
AUTHOR:str = "ByteCorum"
URL:str  = "https://github.com/ByteCorum/pyguard"
VERSION:str  = "3.1.0.0"
DESCRIPTION:str  = "PyGuard is a Python obfuscation and anti-tampering library. It protects from decompilation, static analysis, reverse engineering, and antivirus analysis"
COMMANDS_DIR:str = f"{path.dirname(path.abspath(__file__))}/commands/"
EXECUTOR_TEMPLATE:str = f"{path.dirname(path.abspath(__file__))}/templates/executor.py"
DEPENDENCIES:list[str]  = ["cryptography", "pycryptodome", "cython", "nuitka", "colorama", "types-colorama","setuptools"]

class Command(ABC):

    def ValidateParams(self) -> None:
        ...

    exclusiveOptions: list[str | list[str]]
    requiredOptions: list[str | list[str]]
    options: dict[str , bool | int | str | list[str]]
    help: str

# class Name_of_the_command(Command): #note: only first letter should be capital
#     def __init__(self): #command handler that will be called when the command is executed
#         pass
#
#      # this function should validate parameters and parameters type
#      # you must validate parameters type to avoid runtime errors or unexpected behavior, because every option in options can have any type between str , bool | int | str | list[str]
#      # you should not validate default parameters because they already validated for you
#      def ValidateParams(self) -> None:
#         pass
#
#     #May be left not initialized if your command has no options#
#     exclusiveOptions: list[str | list[str]] = [["--install","--uninstall"], ["--up","--down"]] #groups of options that can't be used together
#     requiredOptions: list[str | list[str]] = ["entrypoint", [""]] #options and groups(any option from a group is required) that are required
#
#     options: dict[str , bool | int | str | list[str]] = { #all the options that your command has. note: don't write help here, it's handled elsewhere
#         #General Options
#         "--quiet": False,
#         "--log": "",
#         "--no-color": False,
#         "--no-input": False,
#
#         #Your Options
#         "--option1": False,
#         "entrypoint": "" #only 1 fixed option name used to store program entrypoint file path
#     }
#
#     #Should be always initialized#
#     help: str = f'''I\'ll help u''' #help message for the command
#
