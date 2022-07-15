from commands import Command
from library import settings
from pathlib import Path

import os, requests

def listScripts(args):
    # 0 - Local, 1 - Online
    serverChosen = 0
    if args is not None:
        argsArray = args.split("\"")
        server = argsArray[0].lower()

        if server == "online":
            serverChosen = 1
            print("Online scripts list chosen.")
        elif server == "local":
            serverChosen = 0
            print("Local scripts list chosen.")
        else:
            serverChosen = 0
            print("Unknown server specified. Defaulting to local...")
    else:
        print("No server specified, defaulting to local.")

    if serverChosen == 0:
        scriptListFile = Path(settings.scriptListDir)
        if scriptListFile.is_file():
            print("Local Script Lists: ")
            print("Format:\n\033[1m[#] - \033[1;2;32m[SCRIPT_NAME]\033[m by \033[1;37m[AUTHOR]\033[m: \033[1m["
                  "DESCRIPTION]\033[m")

            scriptListFile = open(settings.scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()

            listFileContents = scriptListFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptNo = listFileContents.index(i)
                scriptDetails = i.split(",")

                scriptName = scriptDetails[1]
                scriptDesc = scriptDetails[3]
                scriptAuthor = scriptDetails[6]

                print('\033[1m[{n}] - \033[1;2;32m{sn}\033[m by \033[1;37m{a}\033[m : \033[1m{d}\033[m'
                      .format(n=scriptNo, sn=scriptName, a=scriptAuthor, d=scriptDesc))
            scriptListFile.close()
        else:
            print("Local scripts list missing. Do -updatescriptlist .")
    elif serverChosen == 1:
        tmpFile = Path(settings.tempDir)

        if tmpFile.is_dir():
            tmpFile = Path(settings.tempDir + "/list.pgettmp")

            if tmpFile.is_file():
                os.remove(settings.tempDir + "/list.pgettmp")

            tmpFile = open(settings.tempDir + "/list.pgettmp", "w+")

            tmpFile.write(requests.get(settings.script_List_Location).content.decode("utf8"))
        else:
            os.mkdir(settings.tempDir)
            tmpFile = open(settings.tempDir + "/list.pgettmp", "w+")
            tmpFile.write(requests.get(settings.script_List_Location).content.decode("utf8"))

        print("Online Script Lists: ")

        tmpFile = open(settings.tempDir + "/list.pgettmp", "r")
        tmpFileContent = tmpFile.read()

        listFileContents = tmpFileContent.split("--")
        listFileContents.pop(0)

        for i in listFileContents:
            scriptNo = listFileContents.index(i)
            scriptDetails = i.split(",")

            scriptName = scriptDetails[1]
            scriptDesc = scriptDetails[3]
            scriptAuthor = scriptDetails[6]

            print('\033[1m[{n}] - \033[1;2;32m{sn}\033[m by \033[1;37m{a}\033[m : \033[1m{d}\033[m'
                  .format(n=scriptNo, sn=scriptName, a=scriptAuthor, d=scriptDesc))
        tmpFile.close()
        os.remove(settings.tempDir + "/list.pgettmp")

class ListCMD(Command.Command):
    def __init__(self) -> None:
        super().__init__("list", "Lists all available scripts to be downloaded either from local script lists or online")

    def run(self, args):
        listScripts(args)

    def getUsage(self):
        return "\033[1mlist\033[m <\033[31mlocal\033[m|\033[31monline\033[m>"

    def getInfo(self):
        return "Usage: \033[1mlist\033[m <\033[31mlocal\033[m|\033[31monline\033[m>\nExample: list local"

    
