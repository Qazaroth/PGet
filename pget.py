from pathlib import Path
from os import system, name
from bin.download import Downloader
from time import sleep

import os
import shutil
import sys
import requests

binDir = "./bin"
scriptsDir = "./scripts"
tempDir = "./temp"

configDir = "{b}/config.pget".format(b=binDir)
hashDir = "{b}/hash.txt".format(b=binDir)
scriptListDir = "{b}/list.txt".format(b=scriptsDir)

updateBat = "updater.bat"

upgrade_Hash_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/hash.txt"
script_List_Location = "https://raw.githubusercontent.com/Qazaroth/pget-list/master/master.txt"


def clear():
    if name == "nt":
        system("cls")
    else:
        system('clear')


def init():
    clear()
    hashFile = Path(hashDir)

    print("Checking if hash file exists...")
    if hashFile.is_file():
        print("Hash file exists.")

        scriptDir = Path(scriptsDir)

        if not scriptDir.is_dir():
            os.mkdir(scriptsDir)

        scriptListFile = Path(scriptListDir)

        if not scriptListFile.is_file():
            scriptListFile = open(scriptListDir, "w+")
            scriptListFile.write(requests.get(script_List_Location).content.decode("utf8"))

        tmpDir = Path(tempDir)

        if not tmpDir.is_dir():
            os.mkdir(tempDir)

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

            try:
                autoUpdate = int(configs[1][11:])

                print("Checking to see if autoUpdate is enabled...")
                if autoUpdate == 1:
                    print("AutoUpdate is enabled.Checking for new updates...")
                    onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
                    localHashFile = open(hashDir, "r+")
                    localHash = localHashFile.read()

                    if localHash == onlineHash:
                        print("Your PGet is currently up-to-date. No updates needed.")
                    else:
                        print("There is a newer version on Github! Please run updater.bat...")
                else:
                    print("AutoUpdate is disabled.")
            except ValueError:
                print("An error occurred while attempting to read config.pget... Please delete the file and restart "
                      "PGet.")
    else:
        print("Please redownload PGet from Github...")


def main():
    clear()
    print("---------------------------------------------------------------------------")
    print("Usage: -command {args}")
    print("\033[1m-get\033[m \033[31m\"SCRIPT_NAME\"\033[m")
    print("\033[1m-update\033[m {\033[31m\"SCRIPT_NAME\"\033[m|\033[31m\"all\"\033[m}")
    print("\033[1m-delete\033[m {\033[31m\"SCRIPT_NAME\"\033[m|\033[31m\"all\"\033[m}")
    print("\033[1m-updatescriptlist\033[m")
    print("\033[1m-list\033[m {\033[31mlocal\033[m|\033[31monline\033[m}")
    print("\033[1m-exit\033[m")
    print("---------------------------------------------------------------------------")
    cmdInputRaw = input("Command: ")
    cmdInput = cmdInputRaw.split()
    cmd = cmdInput[0].lower()
    args = cmdInputRaw[cmd.__len__()::].strip() or None

    if cmd == "-delete":
        argsArray = args.split("\"")
        inpScriptName = argsArray[1]

        if inpScriptName.lower() == "all":
            print("Deleting everything in scripts folder.")
            for i in os.listdir(scriptsDir):
                deleteThisDir = scriptsDir + "/" + i
                try:
                    shutil.rmtree(deleteThisDir)
                except NotADirectoryError:
                    os.remove(deleteThisDir)
            print("Deleted everything in scripts folder.")
        else:
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
    elif cmd == "-list":
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
            scriptListFile = Path(scriptListDir)
            if scriptListFile.is_file():
                print("Local Script Lists: ")
                print("Format:\n\033[1m[#] - \033[1;2;32m[SCRIPT_NAME]\033[m by \033[1;37m[AUTHOR]\033[m: \033[1m["
                      "DESCRIPTION]\033[m")

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

                    print('\033[1m{n} - \033[1;2;32m{sn}\033[m by \033[1;37m{a}\033[m : \033[1m{d}\033[m'
                          .format(n=scriptNo, sn=scriptName, a=scriptAuthor, d=scriptDesc))
                scriptListFile.close()
            else:
                print("Local scripts list missing. Do -updatescriptlist .")
        elif serverChosen == 1:
            tmpFile = Path(tempDir)

            if tmpFile.is_dir():
                tmpFile = Path(tempDir + "/list.pgettmp")

                if tmpFile.is_file():
                    os.remove(tempDir + "/list.pgettmp")

                tmpFile = open(tempDir + "/list.pgettmp", "w+")

                tmpFile.write(requests.get(script_List_Location).content.decode("utf8"))
            else:
                os.mkdir(tempDir)
                tmpFile = open(tempDir + "/list.pgettmp", "w+")
                tmpFile.write(requests.get(script_List_Location).content.decode("utf8"))

            print("Online Script Lists: ")

            tmpFile = open(tempDir + "/list.pgettmp", "r")
            tmpFileContent = tmpFile.read()

            listFileContents = tmpFileContent.split("--")
            listFileContents.pop(0)

            for i in listFileContents:
                scriptNo = listFileContents.index(i)
                scriptDetails = i.split(",")

                scriptName = scriptDetails[1]
                scriptDesc = scriptDetails[3]
                scriptAuthor = scriptDetails[6]

                print('\033[1m{n} - \033[1;2;32m{sn}\033[m by \033[1;37m{a}\033[m : \033[1m{d}\033[m'
                      .format(n=scriptNo, sn=scriptName, a=scriptAuthor, d=scriptDesc))
            tmpFile.close()
            os.remove(tempDir + "/list.pgettmp")
    elif cmd == "-update":
        argsArray = args.split("\"")
        inpScriptName = argsArray[1]

        scriptListFile = Path(scriptListDir)

        if inpScriptName.lower() == "all":
            print("Please wait...")
            if scriptListFile.is_file():
                scriptListFile = open(scriptListDir, "r")
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
                                    Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
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
                scriptListFile = open(scriptListDir, "r")
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
                                        Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
                                        tmpFile = open(hashScriptDir, "w+")
                                        tmpFile.write(scriptHash)
                                        tmpFile = open(batScriptDir, "w+")
                                        tmpFile.write(
                                            "@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                    a=scriptAuthor,
                                                                                                    f=file_name))
                                        print("Updated {f}.".format(f=file_name, a=scriptAuthor))
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

                if catDir.is_dir():
                    if inpScriptName == scriptName:
                        file_name = scriptURL.split("/")[-1]
                        dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                        hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                        batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName, f=scriptName)

                        scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                        tmpFile = Path(scriptDir)

                        if not tmpFile.is_dir():
                            print("Downloading \033[1;2;32m{f}\033[m] by \033[1;37m{a}\033[m]...".format(f=file_name,
                                                                                                         a=scriptAuthor)
                                  )
                            os.mkdir(scriptDir)
                            Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
                            tmpFile = open(hashScriptDir, "w+")
                            tmpFile.write(scriptHash)
                            tmpFile = open(batScriptDir, "w+")
                            tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                  a=scriptAuthor,
                                                                                                  f=file_name))
                            print("Downloaded \033[1;2;32m{f}\033[m] by \033[1;37m{a}\033[m].".format(f=file_name,
                                                                                                      a=scriptAuthor))
                        else:
                            print("\033[1;2;32m{f}\033[m] already exists..".format(f=scriptName))
                        tmpFile.close()
                        break
                else:
                    if inpScriptName == scriptName:
                        os.mkdir(catDir)
                        file_name = scriptURL.split("/")[-1]
                        dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                        hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                        batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName, f=scriptName)

                        scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                        tmpFile = Path(scriptDir)

                        if not tmpFile.is_dir():
                            print("Downloading \033[1;2;32m{f}\033[m] by \033[1;37m{a}\033[m]...".format(f=file_name,
                                                                                                         a=scriptAuthor)
                                  )
                            os.mkdir(scriptDir)
                            Downloader.downloadScriptNoOutput(Downloader, scriptURL, dir)
                            tmpFile = open(hashScriptDir, "w+")
                            tmpFile.write(scriptHash)
                            tmpFile = open(batScriptDir, "w+")
                            tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                  a=scriptAuthor,
                                                                                                  f=file_name))
                            print("Downloaded \033[1;2;32m{f}\033[m] by \033[1;37m{a}\033[m].".format(f=file_name,
                                                                                                      a=scriptAuthor))
                        else:
                            print("\033[1;2;32m{f}\033[m] already exists..".format(f=scriptName))
                        tmpFile.close()
                        break
            scriptListFile.close()
        else:
            print("Local script lists missing... Do -updatescriptlist .")
    elif cmd == "-updatescriptlist":
        print("Updating local scripts list...")
        scriptListFile = open(scriptListDir, "w+")
        scriptListFile.write(requests.get(script_List_Location).content.decode("utf8"))
        scriptListFile.close()
        print("Updated local scripts list.")
    elif cmd == "-exit":
        print("Stopping pget...")
        sys.exit(0)

    sleep(2)
    input("Press ENTER to continue...")
    main()


init()
sleep(2)
main()
