from commands import Command
from scriptFunctions import downloadFile, settings
from pathlib import Path

def updateScripts(args):
    argsArray = args.split("\"")
    inpScriptName = argsArray[0]

    scriptListFile = Path(settings.scriptListDir)

    if inpScriptName.lower() == "all":
        print("Please wait...")
        if scriptListFile.is_file():
            scriptListFile = open(settings.scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContent = scriptListFileContent.split("--")
            listFileContent.pop(0)

            for i in listFileContent:
                scriptDetails = i.split(",")
                scriptName = scriptDetails[1]
                scriptURL = scriptDetails[2]
                scriptHash = scriptDetails[5]
                scriptAuthor = scriptDetails[6]
                scriptCategory = scriptDetails[7]

                catDir = "./scripts/{c}".format(c=scriptCategory)
                catDir = Path(catDir)

                if catDir.is_dir():
                    file_name = scriptURL.split("/")[-1]
                    dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                    hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                    batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName,
                                                                      f=scriptName)

                    scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)
                    scriptHashDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)

                    tmpFile = Path(scriptDir)

                    if tmpFile.is_dir():
                        print("Script \033[1m{f}\033[m exists... Checking for updates...".format(f=scriptName))
                        tmpFile = Path(scriptHashDir)

                        if tmpFile.is_file():
                            tmpFile = open(scriptHashDir, "r")

                            localHashFile = tmpFile.read()

                            if localHashFile == scriptHash:
                                print("There is either no new update for \033[1m{f}\033[m or your script list is "
                                      "not updated.".format(f=scriptName))
                            else:
                                print("There is a new update! Updating {f}...".format(f=scriptName))
                                downloadFile(scriptURL, dir, True)
                                tmpFile = open(hashScriptDir, "w+")
                                tmpFile.write(scriptHash)
                                tmpFile = open(batScriptDir, "w+")
                                tmpFile.write(
                                    "@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                            a=scriptAuthor,
                                                                                            f=file_name))
                                print("Updated \033[1m{f}\033[m.".format(f=file_name, a=scriptAuthor))
    else:
        if scriptListFile.is_file():
            scriptListFile = open(settings.scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContent = scriptListFileContent.split("--")
            listFileContent.pop(0)

            for i in listFileContent:
                scriptDetails = i.split(",")
                scriptName = scriptDetails[1]
                scriptURL = scriptDetails[2]
                scriptHash = scriptDetails[5]
                scriptAuthor = scriptDetails[6]
                scriptCategory = scriptDetails[7]

                catDir = "./scripts/{c}".format(c=scriptCategory)
                catDir = Path(catDir)

                if catDir.is_dir():
                    if inpScriptName == scriptName:
                        file_name = scriptURL.split("/")[-1]
                        dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                        hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                        batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName,
                                                                          f=scriptName)

                        scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)
                        scriptHashDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)

                        tmpFile = Path(scriptDir)

                        if tmpFile.is_dir():
                            print("File exists... Checking for updates...")
                            tmpFile = Path(scriptHashDir)

                            if tmpFile.is_file():
                                tmpFile = open(scriptHashDir, "r")

                                localHashFile = tmpFile.read()

                                if localHashFile == scriptHash:
                                    print("There is either no new update or your script list is not updated.")
                                else:
                                    print("There is a new update! Updating {f}...".format(f=scriptName))
                                    downloadFile(scriptURL, dir, True)
                                    tmpFile = open(hashScriptDir, "w+")
                                    tmpFile.write(scriptHash)
                                    tmpFile = open(batScriptDir, "w+")
                                    tmpFile.write(
                                        "@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                a=scriptAuthor,
                                                                                                f=file_name))
                                    print("Updated {f}.".format(f=file_name, a=scriptAuthor))

class UpdateScriptsCMD(Command.Command):
    def __init__(self) -> None:
        super().__init__("updates", "Updates either specified script or everything in \"scripts\" folder.")

    def run(self, args):
        updateScripts(args)

    def getUsage(self):
        return "\033[1mupdate\033[m <\033[31mSCRIPT_NAME\033[m|\033[31mall\033[m>"

    def getInfo(self):
        return "Usage: \033[1mupdate\033[m <\033[31mSCRIPT_NAME\033[m|\033[31mall\033[m>\nExample: update all"

    
