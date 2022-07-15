from commands import Command, CommandHandler
from InquirerPy import inquirer
from time import sleep
from library.utils import *

class HelpCMD(Command.Command):
    def __init__(self, cmdHandler : CommandHandler.CommandHandler() = None) -> None:
        super().__init__("help", "Displays info about specified command")
        if cmdHandler is None:
            self.__cmdHandler = CommandHandler.CommandHandler()
            self.__cmdHandler.addCommand(self.getName(), self)
        else:
            self.__cmdHandler = cmdHandler

    def run(self, args):
        cmds = self.__cmdHandler.getCommands()
        cmdList = [k for k in cmds]

        selectedCmd = inquirer.select(
            message="Which command would you like to know more of?",
            choices=cmdList,
        ).execute()

        clear()
        c : Command.Command() = cmds[selectedCmd]
        print("Information for {}".format(selectedCmd))
        print("-" * 75)
        print(c.getDescription())
        print("-" * 75)
        print(c.getInfo())
        sleep(2)

    def getUsage(self):
        return "\033[1mhelp\033[m"

    def getInfo(self):
        return "Usage: \033[1mhelp\033[m [\033[31mCOMMAND\033[m]"

    
