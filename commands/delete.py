from commands import Command
from scriptFunctions import downloadFile, settings
from pathlib import Path

import os, shutil

def deleteScripts(args):
    argsArray = args.split("\"")
    inpScriptName = argsArray[0]

    if inpScriptName.lower() == "all":
        print("Deleting everything in scripts folder.")
        for i in os.listdir(settings.scriptsDir):
            deleteThisDir = settings.scriptsDir + "/" + i
            try:
                shutil.rmtree(deleteThisDir)
            except NotADirectoryError:
                os.remove(deleteThisDir)
        print("Deleted everything in scripts folder.")
    else:
        print("Checking if script {s} exists...".format(s=inpScriptName))
        scriptListFile = Path(settings.scriptListDir)

        if scriptListFile.is_file():
            scriptListFile = open(settings.scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContents = scriptListFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptDetails = i.split(",")
                scriptName = scriptDetails[1]
                scriptCategory = scriptDetails[7]

                if inpScriptName == scriptName:
                    print("{f} script exists in database, now checking if it's downloaded locally...".format(
                        f=scriptName
                    ))
                    scriptDirS = "./scripts/{c}/{s}".format(c=scriptCategory, s=scriptName)
                    scriptDir = Path(scriptDirS)

                    if scriptDir.is_dir():
                        print("Script {f} is downloaded locally, deleting...".format(f=scriptName))
                        shutil.rmtree(scriptDirS)
                        print("Deleted {f}.".format(f=scriptName))
                        break
            scriptListFile.close()
        else:
            print("Scripts list file missing, please do -updatescriptlist.")

class DeleteScriptsCMD(Command.Command):
    def __init__(self) -> None:
        super().__init__("delete", "Deletes either specified script or everything in \"scripts\" folder.")

    def run(self, args):
        deleteScripts(args)

    def getUsage(self):
        return "\033[1mdelete\033[m <\033[31mSCRIPT_NAME\033[m|\033[31mall\033[m>"

    def getInfo(self):
        return "Usage: \033[1mdelete\033[m <\033[31mSCRIPT_NAME\033[m|\033[31mall\033[m>\nExample: delete all"

    
