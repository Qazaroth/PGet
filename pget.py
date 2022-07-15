from pathlib import Path
from os import system, name, path
from commands.Command import Command
from library.download import downloadFile
from library import settings
from time import sleep

from scriptFunctions import *

import subprocess

try:
    import requests
except ModuleNotFoundError:
    subprocess.run(["pip install requests"])

import os

from commands import fetch, updatescriptlist, exit, list, delete, update

f = fetch.FetchCMD()
d = delete.DeleteScriptsCMD()
up = update.UpdateScriptsCMD()
u = updatescriptlist.UpdateScriptList()
e = exit.ExitCMD()
l = list.ListCMD()

separator = "-" * 75
commands = {}

commands[f.getName()] = f
commands[d.getName()] = d
commands[up.getName()] = up
commands[l.getName()] = l
commands[u.getName()] = u
commands[e.getName()] = e

def clear():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"

    os.system(command)


def printTitle():
    versionFile = Path(settings.binDir + "/version.txt")
    version = "v6.6.6-yourecursed"

    if versionFile.is_file():
        versionFile = open(settings.binDir + "/version.txt", "r")
        version = versionFile.read().splitlines()[0]

    print(separator)
    print("""
        ██████╗  ██████╗ ███████╗████████╗
        ██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝
        ██████╔╝██║  ███╗█████╗     ██║   
        ██╔═══╝ ██║   ██║██╔══╝     ██║   
        ██║     ╚██████╔╝███████╗   ██║   
        ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   v{}""".format(version))
    print(separator)
    print("Usage: -command {args}")
    for key in commands:
        v : Command = commands[key]
        print(" {} - {}".format(v.getUsage(), v.getDescription()))
    print(separator)


def main():
    clear()
    printTitle()
    cmdInputRaw = input("Command: ")
    cmdInput = cmdInputRaw.split()

    if cmdInput.__len__() > 0:
        cmd = cmdInput[0].lower()
        args = cmdInputRaw[cmd.__len__()::].strip() or None

        c = commands.get(cmd, None)
        if c is not None:
            c.run(args)
    else:
        print("No command inputted...")

    sleep(2)
    input("Press ENTER to continue...")
    main()


def init():
    canRun = False
    clear()

    hashFile = Path(settings.hashDir)

    if settings.debugMode:
        print("Checking if hash file exists...")

    if hashFile.is_file():
        if settings.debugMode:
            print("Hash file exists.")

        scriptDir = Path(settings.scriptsDir)

        if not scriptDir.is_dir():
            os.mkdir(settings.scriptsDir)

        tmpDir = Path(settings.tempDir)

        if not tmpDir.is_dir():
            os.mkdir(settings.tempDir)

        if settings.debugMode:
            print("Checking if config.pget exists...")

        configFile = Path(settings.configDir)

        if not configFile.is_file():
            if settings.debugMode:
                print("config.pget does not exist... making one...")
            configFile = open(settings.configDir, "w+")
            configFile.write("[DO NOT DELETE]\n")
            configFile.write("autoUpdate=0\n")
            configFile.write("createLocalScriptList=0")
            if settings.debugMode:
                print("Made config.pget. Do not delete this file!")
            canRun = True
        else:
            if settings.debugMode:
                print("config.pget exist! Do not delete this file!")
            configFile = open(settings.configDir, "r")
            configs = configFile.read().splitlines()

            try:
                if configs.__sizeof__() > 0:
                    autoUpdate = int(configs[1][11:])
                    createLocalScriptList = int(configs[2][22:])

                    if settings.debugMode:
                        print("Checking to see if autoUpdate is enabled...")

                    if autoUpdate == 1:
                        if settings.debugMode:
                            print("AutoUpdate is enabled.Checking for new updates...")
                        onlineHash = requests.get(settings.upgrade_Hash_Location).content.decode("utf8")
                        localHashFile = open(settings.hashDir, "r+")
                        localHash = localHashFile.read()

                        if localHash == onlineHash:
                            print("Your PGet is currently up-to-date. No updates needed.")
                        else:
                            print("There is a newer version on Github! Please run updater.bat...")
                    else:
                        if settings.debugMode:
                            print("AutoUpdate is disabled.")

                    if createLocalScriptList == 1:
                        scriptListFile = Path(settings.scriptListDir)

                        if not scriptListFile.is_file():
                            scriptListFile = open(settings.scriptListDir, "w+")
                            scriptListFile.write(requests.get(settings.script_List_Location).content.decode("utf8"))
            except ValueError:
                print("An error occurred while attempting to read config.pget... Please delete the file and restart "
                      "PGet.")
            canRun = True

        sleep(2)

        if canRun:
            main()
    else:
        print("Please redownload PGet from Github...")

init()