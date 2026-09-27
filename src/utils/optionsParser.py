from utils.logger import Log
from config import Command

class OptionsParser:
    def __init__(self, argv: list[str], command: Command) -> None:
        self.argv: list[str] = argv
        self.argc: int = len(self.argv)
        self.command: Command = command
        self.helpCalled: bool = False # handles the --help command with the highest priority

    def InitCommandParams(self) -> None:
        # Highest priority for help
        if "--help" in self.argv:
            if self.argc > 1:
                Log.Warning("--help found, other options ignored.")
            self.helpCalled = True
            return

        skipNext = False # Some params have value like <param-name> <value>, this var determinate whether next obj is param(False) and not value(True)

        for i in range(0, self.argc):
            # Skip current obj, cuz it was logged as value of previous param
            if skipNext:
                skipNext = False
                continue

            option:str = self.argv[i]

            # Check for main file "entrypoint", special check cuz it always goes in the end of the file and does't match expected option
            if "entrypoint" in self.command.options and i == self.argc-1 and option.find(".py") != -1:
                self.command.options["entrypoint"] = option
                continue

            # Check whether option in dict options under command, for understanding see obfuscate.py command
            if option not in self.command.options:
                raise Exception(f"invalid option: \"{option}\".")

            # Gives value of an option to check whether it has default value or smt else
            if OptionsParser.__CheckOptionValue(self.command.options[option]):
                Log.Warning(f"Value overridden, \"{option}\" have been already defined.")

            # If it's bool just set it to true
            if type(self.command.options[option]) == bool:
                self.command.options[option] = True

            else:
                # If it's not a bool it should has a value
                # It doesn't check the correctness of passed value, cuz it's job of command itself, just it's existence
                if i+1 >= self.argc or self.argv[i+1].find("--") != -1:
                    raise Exception(f"invalid \"{option}\" value.")

                value:str = self.argv[i+1]
                expectedValueType: type[bool|str|int|list[str]] =  type(self.command.options[option])

                #Program assume that value have the same type as expectedValueType and tries to convert to needed type and should fail with exception if types don't match
                if expectedValueType == str:
                    self.command.options[option] = value
                elif expectedValueType == int:
                    self.command.options[option] = int(value)
                elif expectedValueType == list[str]:
                    self.command.options[option] = value.split(",")
                else:
                    raise Exception(f"internal error: expectedValueType({expectedValueType}) doesn't match any known type")

                skipNext = True

    def ValidateParams(self) -> None:
        if self.command.requiredOptions:
            for option in self.command.requiredOptions:
                # One from many variants
                if type(option) == list:
                    inited = False# Is at least one inited correctly

                    for opt in option:
                        # Gives value of an option to check whether it has default value or smt else
                        if OptionsParser.__CheckOptionValue(self.command.options[opt]):
                            inited = True
                            break

                    if not inited:
                        raise Exception(f"at least one of this options required: \"{", ".join(option)}\".")

                # One particular option
                else:
                    # Gives value of an option to check whether it has default value or smt else
                    # pyrefly: ignore [bad-index] - option can not be list cuz already checked
                    if not OptionsParser.__CheckOptionValue(self.command.options[option]):
                        raise Exception(f"missing required option: \"{option}\".")

        if self.command.exclusiveOptions:
            for group in self.command.exclusiveOptions:
                state: list[bool] = []# state of option 0(off), 1(on)
                for option in group:
                    # Gives value of an option to check whether it has default value or smt else
                    state.append(OptionsParser.__CheckOptionValue(self.command.options[option]))

                #More than 1 only if more than one are on =)
                if sum(state) > 1:
                    raise Exception(f"some options can't be used together: \"{", ".join(group)}\".")

    @staticmethod
    # True if initialized
    def __CheckOptionValue(option: bool|int|str|list[str]) -> bool:
        optionType: type[bool|str|int|list[str]] = type(option)

        if optionType == bool:
            if option == False:
               return False

        elif optionType == str:
            if option == "":
               return False

        elif optionType == int:
            if option == 0:
                return False

        elif optionType == list[str]:
            if option == []:
                return False
        else:
            raise Exception(f"internal error: optionType({optionType}) doesn't match any known type")

        return True
