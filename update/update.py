from pathlib import Path

import sys
import os
import requests

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from library.download import downloadFile

upgrade_Hash_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/hash.txt"
upgrade_Script_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/update/update.py"
pget_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/pget.py"
readme_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/README.md"
version_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/version.txt"
downloadpy_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/download.py"

mainDir = "./"
mainDir2 = "../"

hashFileExists = False
versionFileExists = False
whichDir = 1

binDir = "bin"
scriptsDir = "scripts"
updateDir = "update"

configDir = "/config.pget"
hashDir = "/hash.txt"

print("Checking if there is new update...")
hashFile = Path(mainDir + "bin/hash.txt")
versionFile = None

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

if whichDir == 1:
    versionFile = Path(mainDir + "bin/version.txt")

    if versionFile.exists():
        versionFileExists = True
else:
    versionFile = Path(mainDir2 + "bin/version.txt")

    if versionFile.exists():
        versionFileExists = True


if hashFileExists and versionFileExists:
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
    versionDir = binDir + "/version.txt"

    onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
    onlineVersion = requests.get(version_location).content.decode("utf8")

    localHashFile = open(hashDir, "r+")
    localVersionFile = open(versionDir, "r+")

    localHash = localHashFile.read()
    localVersion = localVersionFile.read()

    onlineVersions = onlineVersion.split("-")
    localVersions = localVersion.split("-")

    if int("".join(onlineVersions[0].split("."))) < int("".join(localVersions[0].split("."))):
        print("[GRACEFUL] An error has occured while trying to update PGet!")
        print("You have either tampered with the bin folders or received earlier update directly from the developer!")
    else:
        if localHash == onlineHash:
            print("There are currently no new updates.")
        else:
            localHashFile.close()
            print("There's a new update! Downloading...")

            downloadFile(upgrade_Hash_Location, hashDir)
            downloadFile(pget_location, md + "/pget.py")
            downloadFile(readme_location, md + "/README.md")
            downloadFile(version_location, binDir + "/version.txt")
            downloadFile(upgrade_Script_Location, updateDir + "/update.py")
            downloadFile(downloadpy_location, binDir + "/download.py")

            print("Successfully updated PGet!")
else:
    print("Missing hash and/or version file. Please re-download from github!")
