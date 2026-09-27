from colorama import Fore
from sys import exit

class Log:
    logFile: str = ""
    quiet: bool = False
    noInput: bool = False
    colored: bool = True

    @staticmethod
    def __Show(prefix: str, message: str, prefixColor: str =Fore.RESET, msgColor: str =Fore.RESET, end: str = '\n') -> None:
        if Log.logFile:
            Log.WriteLog(f"{prefix}{message}", end)
        if Log.colored:
            print(f"{prefixColor}{prefix}{Fore.RESET}{msgColor}{message}{Fore.RESET}", end=end)
        else:
            print(f"{prefix}{message}", end=end)

    @staticmethod
    def WriteLog(message: str, end: str = '\n') -> None:
        try:
            with open(Log.logFile, "a") as file:
                file.write(f"{message}{end}")
        except Exception as error:
            Log.logFile = ""
            Log.Warning(f"Logging skipped: {error}", True)

    @staticmethod
    def Info(message: str, bypassQuiet: bool =False) -> None:
        if Log.quiet and not bypassQuiet:
            return
        Log.__Show("[i]", message, prefixColor=Fore.CYAN)

    @staticmethod
    def Warning(message: str, pause: bool =False) -> None:
        if Log.quiet and not pause:
            return

        Log.__Show("[!]", message, prefixColor=Fore.YELLOW)
        if pause and not Log.noInput:
            input("Press any key to continue...")

    @staticmethod
    def Fail(message: str, fatal: bool =False) -> None:
        Log.__Show("[x]", message, prefixColor=Fore.RED)
        if fatal:
            exit(1)

    @staticmethod
    def Success(message: str, bypassQuiet: bool =False) -> None:
        if Log.quiet and not bypassQuiet:
            return
        Log.__Show("[+]", message, prefixColor=Fore.GREEN)

    @staticmethod
    def Question(message: str) -> str:
        if Log.quiet and Log.noInput:
            return "ignored"

        Log.__Show("[?]", message, prefixColor=Fore.BLUE)
        Log.__Show(">>>", " ", prefixColor=Fore.BLUE, end='')

        if not Log.noInput:
            response:str = input()
        else:
            response:str = "ignored"

        Log.Custom(response)

        return response

    @staticmethod
    def Custom(message: str, color: str =Fore.RESET, bypassQuiet: bool =False, end: str ='\n') -> None:
        if Log.quiet and not bypassQuiet:
            return
        Log.__Show("", message, msgColor=color, end=end)
