from types import ModuleType
from importlib.machinery import ModuleSpec
from sys import argv, exit
from os import walk
from inspect import isclass, isabstract
from importlib.util import spec_from_file_location, module_from_spec

from utils.optionsParser import OptionsParser
from utils.logger import Log
from config import Command, NAME, COMMANDS_DIR


class PyGuard:
    command: Command
    helpCmd: Command

    def __init__(self) -> None:
        try:
            self.helpCmd = self.GetCommand("help")
            self.ParseArgs()
            self.SetGlobalVars()
            self.RunCommand()
        except Exception as error:
            Log.Fail(f"Fatal error occurred: {error}", True)

    def ParseArgs(self) -> None:
        try:
            # Call should contain at least executable path and command name
            if len(argv) < 2:
                raise Exception("missing command name")

            self.command = self.GetCommand(argv[1])

        except Exception as error:
            # helpCmd passed to helpCmd, cuz helpCmd expects a command to get help from
            # pyrefly: ignore [not-callable] - this is required, cuz pyrefly can't check not directly imported command
            self.helpCmd(self.helpCmd)
            Log.Fail("Command parsing failed: "+str(error), True)

        try:
            # Only initialize parser
            parser = OptionsParser(argv[2:], self.command)
            # Parses and fills values in self.command's options dict
            parser.InitCommandParams()

            # Highest priority for help
            if parser.helpCalled:
                # pyrefly: ignore [not-callable] - this is required, cuz pyrefly can't check not directly imported command
                self.helpCmd(self.command)
                exit(0)

            parser.ValidateParams()

        except Exception as error:
            Log.Fail(f"Options parsing failed: {error}", True)

    def GetCommand(self, name:str) -> Command:
        #name.title(), cuz it looks in files in commands/** for class name, which is title by project style
        command: Command | None = self.SearchCommand(name.title(), COMMANDS_DIR)
        if not command:
            raise Exception(f"invalid command name: \"{name.lower()}\"")

        return command

    def SearchCommand(self, name: str, path: str) -> Command | None:
        for dirpath, dirnames, filenames in walk(path):
            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":

                    filePath: str = f"{dirpath}/{filename}"
                    # Create a module "spec" (import metadata) for the file
                    spec: ModuleSpec | None = spec_from_file_location("temp_module", filePath)

                    # Proceed only if the spec exists and has a loader attached (the loader is what actually executes the module's code)
                    if spec and spec.loader:
                        module: ModuleType = module_from_spec(spec)
                        # Create an empty module object from the spec(the code hasn't run yet at this point).

                        try:
                            # Execute the file's code, populating the module object
                            spec.loader.exec_module(module)

                            # Iterate over every attribute name defined in the module.
                            for cmdName in dir(module):

                                # Fetch the actual object behind that name.
                                # Returned value can basically be anything, so type Command is more for static checking
                                command: Command = getattr(module, cmdName)

                                # Actual runtime checks
                                # 1. actual classes,
                                # 2. not abstract,
                                # 3. subclasses of the Command base class,
                                # 4. not the base Command class itself.
                                if (isclass(command) and
                                    not isabstract(command) and
                                    issubclass(command, Command) and
                                    command.__name__ != 'Command'):

                                    if (command.__name__ == name):
                                        return command

                        except Exception as error:
                            # Skip files that can't be imported
                            Log.Warning(f"Command module skipped: {path}: {error}")
                            continue
        return None

    def SetGlobalVars(self) -> None:
        if "--log" in self.command.options:
            if type(self.command.options["--log"]) != str:
                raise Exception(f"invalid \"--log\" variable type: must be \"str\", but it's \"{type(self.command.options["--log"])}\"")

            Log.logFile = self.command.options["--log"]

        if "--quiet" in self.command.options:
            if type(self.command.options["--quiet"]) != bool:
                raise Exception(f"invalid \"--quiet\" variable type: must be \"bool\", but it's \"{type(self.command.options["--quiet"])}\"")
            Log.quiet = self.command.options["--quiet"]

        if "--no-color" in self.command.options:
            if type(self.command.options["--no-color"]) != bool:
                raise Exception(f"invalid \"--no-color\" variable type: must be \"bool\", but it's \"{type(self.command.options["--no-color"])}\"")
            Log.colored = not self.command.options["--no-color"]

        if "--no-input" in self.command.options:
            if type(self.command.options["--no-input"]) != bool:
                raise Exception(f"invalid \"--no-input\" variable type: must be \"bool\", but it's \"{type(self.command.options["--no-input"])}\"")
            Log.noInput = self.command.options["--no-input"]

    def RunCommand(self) -> None:
        Log.Info(f"{NAME}\n")
        try:
            # pyrefly: ignore [not-callable] - this is required, cuz pyrefly can't check not directly imported command
            self.command()
        except Exception as error:
            Log.Fail(f"Command failed: {error}", True)
