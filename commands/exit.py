from commands import Command

import sys

class ExitCMD(Command.Command):
    def __init__(self) -> None:
        super().__init__("exit", "Ends the program")

    def run(self, args):
        print("Stopping PGet...")
        sys.exit(0)

    def getUsage(self):
        return "\033[1mexit\033[m"

    def getInfo(self):
        return "Usage: \033[1mexit\033[m"

    
