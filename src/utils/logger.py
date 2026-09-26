from colorama import Fore
from sys import exit

class Log:
    logFile = ""
    quiet = False
    noInput = False
    colored = True

    @staticmethod
    def Show(prefix, message, color):
        if Log.colored:
            print(f"{color}{prefix}{Fore.RESET}{message}")
        else:
            print(f"{prefix}{message}")

    @staticmethod
    def WriteLog(message):
        if Log.logFile:
            try:
                with open(Log.logFile, "a") as file:
                    file.write(f"{message}\n")
            except Exception as error:
                Log.logFile = ""
                Log.Warning(f"Logging skipped: {error}", True)

    @staticmethod
    def Info(message, bypassQuiet=False):
        Log.WriteLog(f"[i]{message}")
        if Log.quiet and not bypassQuiet:
            return
        Log.Show("[i]", message, Fore.CYAN)

    @staticmethod
    def Warning(message, pause=False):
        Log.WriteLog(f"[!]{message}")
        if Log.quiet and not pause:
            return
        Log.Show("[!]", message, Fore.YELLOW)

        if pause and not Log.noInput:
            input("Press Enter to continue...")

    @staticmethod
    def Fail(message, fatal=False):
        Log.WriteLog(f"[x]{message}")
        Log.Show("[x]", message, Fore.RED)
        if fatal:
            exit(-1)

    @staticmethod
    def Success(message):
        Log.WriteLog(f"[+]{message}")
        Log.Show("[+]", message, Fore.GREEN)

    @staticmethod
    def Question(message) -> str:
        Log.WriteLog(f"[?]{message}")
        if Log.noInput:
            Log.WriteLog(">>> {ignored}")
            return "ignore"

        if Log.colored:
            print(f"{Fore.BLUE}[?]{Fore.RESET}{message}")
            response = input(f"{Fore.BLUE}>>> {Fore.RESET}")
        else:
            print(f"[?]{message}")
            response = input(f">>> ")

        Log.WriteLog(f">>> {response}")
        return response

    @staticmethod
    def Custom(message, color = Fore.RESET, bypassQuiet=False):
        Log.WriteLog(message)
        if Log.quiet and not bypassQuiet:
            return
        Log.Show("", message, color)