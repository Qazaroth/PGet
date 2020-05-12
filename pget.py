from pathlib import Path
from os import system, name
import os
import shutil
import sys
from time import sleep
import requests
from bin.download import Downloader

binDir = "./bin"
scriptsDir = "./scripts"

configDir = "{b}/config.pget".format(b=binDir)
hashDir = "{b}/hash.txt".format(b=binDir)
scriptListDir = "{b}/list.txt".format(b=scriptsDir)

upgrade_Hash_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/hash.txt"
script_List_Location = "https://raw.githubusercontent.com/Qazaroth/pget-list/master/master.txt"


def init():
    hashFile = Path(hashDir)

    print("Checking if hash file exists...")
    if hashFile.is_file():
        print("Hash file exists.")

        scriptListFile = Path(scriptListDir)

        if not scriptListFile.is_file():
            scriptListFile = open(scriptListDir, "w+")
            scriptListFile.write(requests.get(script_List_Location).content.decode("utf8"))

        print("Checking if config.pget exists...")
        configFile = Path(configDir)

        if not configFile.is_file():
            print("config.pget does not exist... making one...")
            configFile = open(configDir, "w+")
            configFile.write("[DO NOT DELETE]\n")
            configFile.write("autoUpdate=0")
            print("Made config.pget. Do not delete this file!")
        else:
            print("config.pget exist! Do not delete this file!")
            configFile = open(configDir, "r")
            configs = configFile.read().splitlines()
            autoUpdate = 0

            try:
                autoUpdate = configs[1]["autoUpdate".__len__() + 1:]
            except ValueError:
                autoUpdate = -1
                print("An error occured while attempting to read config.pget... Please delete the file and restart "
                      "PGet.")

            print("Checking to see if autoUpdate is enabled...")
            if autoUpdate == 1:
                print("AutoUpdate is enabled.Checking for new updates...")
                onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
                localHashFile = open(hashDir, "r+")
                localHash = localHashFile.read()

                if localHash == onlineHash:
                    print("Your PGet is currently up-to-date. No updates needed.")
                else:
                    print("There is a newer version on Github! Please run updater.py.")
            else:
                print("AutoUpdate is disabled.")
    else:
        print("Please get PGet from Github...")


def main():
    if name == "nt":
        system("cls")
    else:
        system('clear')
    print("---------------------------------------------------------------------------")
    print("Usage: -command {args}")
    print("-get \"SCRIPT_NAME\"")
    print("-delete \"SCRIPT_NAME\"")
    print("-updatescriptlist")
    print("-list")
    print("-exit")
    print("---------------------------------------------------------------------------")
    cmdInputRaw = input("Command: ")
    cmdInput = cmdInputRaw.split()
    cmd = cmdInput[0].lower()
    args = cmdInputRaw[cmd.__len__()::].strip() or None

    if cmd == "-delete":
        argsArray = args.split("\"")
        inpScriptName = argsArray[1]
        print("Checking if script {s} exists...".format(s=inpScriptName))
        scriptListFile = Path(scriptListDir)

        if scriptListFile.is_file():
            scriptListFile = open(scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContents = scriptListFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptDetails = i.split(",")
                scriptName = scriptDetails[1]
                scriptURL = scriptDetails[2]
                scriptHash = scriptDetails[5]
                scriptAuthor = scriptDetails[6]
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
        else:
            print("Scripts list file missing, please do -updatescriptlist.")
    elif cmd == "-list":
        scriptListFile = Path(scriptListDir)

        if scriptListFile.is_file():
            print("Script Lists: ")

            scriptListFile = open(scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContents = scriptListFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptNo = listFileContents.index(i)
                scriptDetails = i.split(",")

                scriptName = scriptDetails[1]
                scriptDesc = scriptDetails[3]
                scriptAuthor = scriptDetails[6]

                print("{n} - {sn} by {a}: {d}".format(n=scriptNo,
                                                      sn=scriptName,
                                                      a=scriptAuthor,
                                                     d=scriptDesc))
        else:
            print("Scripts list missing. Do -updatescriptlist .")
    elif cmd == "-get":
        argsArray = args.split("\"")
        inpScriptName = argsArray[1]

        scriptListFile = Path(scriptListDir)

        if scriptListFile.is_file():
            scriptListFile = open(scriptListDir, "r")
            scriptListFileContent = scriptListFile.read()
            listFileContents = scriptListFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptDetails = i.split(",")
                scriptName = scriptDetails[1]
                scriptURL = scriptDetails[2]
                scriptHash = scriptDetails[5]
                scriptAuthor = scriptDetails[6]
                scriptCategory = scriptDetails[7]

                catDir = "./scripts/{c}".format(c=scriptCategory)
                catDir = Path(catDir)

                if not catDir.is_dir():
                    os.mkdir(catDir)

                if inpScriptName == scriptName:
                    file_name = scriptURL.split("/")[-1]
                    dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                    hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)

                    scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                    tmpFile = Path(scriptDir)

                    if not tmpFile.is_dir():
                        print("Downloading {f} by {a}...".format(f=file_name, a=scriptAuthor))
                        os.mkdir(scriptDir)
                        Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
                        scriptHashFile = open("./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory), "w+")
                        scriptHashFile.write(scriptHash)
                        print("Downloaded {f} by {a}.".format(f=file_name, a=scriptAuthor))
                    else:
                        print("{f} already exists... checking for update instead.".format(f=scriptName))
                        scriptHashFile = open("./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory), "r")
                        scriptOldHash = scriptHashFile.read()

                        if scriptOldHash != scriptHash:
                            print("Updating {f} by {a}...".format(f=file_name, a=scriptAuthor))
                            Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
                            scriptHashFile = open("./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory),
                                                  "w+")
                            scriptHashFile.write(scriptHash)
                            print("Updated {f} by {a}.".format(f=file_name, a=scriptAuthor))
                        else:
                            print("You already have the latest version, or update script list.")
                    break
    elif cmd == "-updatescriptlist":
        print("Updating scripts list...")
        scriptListFile = Path(scriptListDir)

        if scriptListFile.is_file():
            scriptListFile = open(scriptListDir, "w+")
            scriptListFile.write(requests.get(script_List_Location).content.decode("utf8"))
        else:
            scriptListFile = open(scriptListDir, "w+")
            scriptListFile.write(requests.get(script_List_Location).content.decode("utf8"))
        print("Updated scripts list.")
    elif cmd == "-exit":
        print("Stopping pget...")
        sys.exit(0)
    input("Press ENTER to continue...")
    main()


init()
sleep(2)
main()
