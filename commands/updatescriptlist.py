from commands import Command
from scriptFunctions import downloadFile, settings

def updatescriptlist(args):
    print("Updating local scripts list...")
    downloadFile(settings.script_List_Location, settings.scriptListDir, True)
    print("Updated local scripts list.")

class UpdateScriptList(Command.Command):
    def __init__(self) -> None:
        super().__init__("updatescriptlist", "Fetches/Downloads the specified script from the \"server\".")

    def run(self, args):
        updatescriptlist(args)

    def getUsage(self):
        return "\033[1mupdatescriptlist\033[m"

    def getInfo(self):
        return "Usage: \033[1mupdatescriptlist\033[m"

    
