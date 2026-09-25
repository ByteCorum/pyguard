from utils.logger import Log
from config import Command

class OptionsParser:
    def __init__(self, argv, command: Command):
        self.argv = argv
        self.argc = len(self.argv)
        self.command = command
        self.helpCalled = False# handles the --help command with the highest priority

    def Parse(self):
        if "--help" in self.argv:
            if self.argc > 1:
                Log.Warning("--help found, other options ignored.")
            self.helpCalled = True
            return

        skipNext = False
        for i in range(0, self.argc):
            if skipNext:
                skipNext = False
                continue

            option = self.argv[i]
            if "entrypoint" in self.command.options and i == self.argc-1 and option.find(".py") != -1:
                self.command.options["entrypoint"] = option
                continue

            if option not in self.command.options:
                raise Exception(f"invalid option: \"{option}\".")

            if OptionsParser.CheckOptionValue(self.command.options[option]):
                Log.Warning(f"Value overridden, \"{option}\" have been already defined.")

            if type(self.command.options[option]) == bool:
                self.command.options[option] = True

            else:
                if i+1 >= self.argc or self.argv[i+1].find("--") != -1:
                    raise Exception(f"invalid \"{option}\" value.")

                value = self.argv[i+1]

                match type(self.command.options[option]).__name__:
                    case "str":
                        self.command.options[option] = value

                    case "int":
                        self.command.options[option] = int(value)

                    case "list":
                        self.command.options[option] = value.split(",")

                    case _:
                        raise Exception(f"unsupported \"{option}\" type.")
                skipNext = True

    def Validate(self):
        for option in self.command.requiredOptions:
            if type(option) == list:
                inited = False# is at least one inited correctly

                for opt in option:
                    if OptionsParser.CheckOptionValue(self.command.options[opt]):
                        inited = True
                        break

                if not inited:
                    raise Exception(f"at least one of this options required: \"{", ".join(option)}\".")

            else:
                if not OptionsParser.CheckOptionValue(self.command.options[option]):
                    raise Exception(f"missing required option: \"{option}\".")

        for group in self.command.exclusiveOptions:
            state = []# state of option 0(off), 1(on)
            for option in group:
                state.append(OptionsParser.CheckOptionValue(self.command.options[option]))

            if sum(state) > 1:
                raise Exception(f"some options can't be used together: \"{", ".join(group)}\".")

    @staticmethod
    def CheckOptionValue(option) -> bool:
        match type(option).__name__:
            case "bool":
                if option == False: return False

            case "str":
                if option == "": return False

            case "int":
                if option == 0:  return False

            case "list":
                if option == []: return False

            case _:
                raise Exception(f"unsupported \"{option}\" type.")

        return True


