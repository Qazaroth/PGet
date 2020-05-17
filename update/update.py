from pathlib import Path

import sys
import os
import requests

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from library.download import Downloader

upgrade_Hash_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/hash.txt"
upgrade_Script_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/update/update.py"
pget_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/pget.py"
readme_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/README.md"
version_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/version.txt"
downloadpy_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/download.py"

mainDir = "./"
mainDir2 = "../"

hashFileExists = False
whichDir = 1

binDir = "bin"
scriptsDir = "scripts"
updateDir = "update"

configDir = "/config.pget"
hashDir = "/hash.txt"

print("Checking if there is new update...")
hashFile = Path(mainDir + "bin/hash.txt")

if hashFile.is_file():
    hashFileExists = True
    whichDir = 1
else:
    hashFile = Path(mainDir2 + "bin/hash.txt")

    if hashFile.is_file():
        hashFileExists = True
        whichDir = 2
    else:
        hashFileExists = False

if hashFileExists:
    binDir = "bin"
    scriptsDir = "scripts"
    updateDir = "update"

    configDir = "/config.pget"
    hashDir = "/hash.txt"

    md = ""

    if whichDir == 1:
        md = mainDir
    elif whichDir == 2:
        md = mainDir2

    binDir = md + "bin"
    scriptsDir = md + "scripts"
    updateDir = md + "update"

    configDir = binDir + "/config.pget"
    hashDir = binDir + "/hash.txt"

    onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
    localHashFile = open(hashDir, "r+")
    localHash = localHashFile.read()

    if localHash == onlineHash:
        print("There are currently no new updates.")
    else:
        localHashFile.close()
        print("There's a new update! Downloading...")

        Downloader.downloadScriptNoOutput(Downloader, upgrade_Hash_Location, hashDir)
        Downloader.downloadScriptNoOutput(Downloader, pget_location, md + "/pget.py")
        Downloader.downloadScriptNoOutput(Downloader, readme_location, md + "/README.md")
        Downloader.downloadScriptNoOutput(Downloader, version_location, binDir + "/version.txt")
        Downloader.downloadScriptNoOutput(Downloader, upgrade_Script_Location, updateDir + "/update.py")
        Downloader.downloadScriptNoOutput(Downloader, downloadpy_location, binDir + "/download.py")

        print("Successfully updated PGet!")
else:
    print("Missing hash file. Please re-download from github!")
