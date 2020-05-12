from pathlib import Path
import urllib.request
import requests

def downloadFile(url, dir):
    file_name = url.split("/")[-1]
    dir = "/{f}".format(f=file_name)

    print("Downloading {scriptName}...".format(scriptName=file_name))

    urllib.request.urlretrieve(url, dir)

def downloadScript(url):
    file_name = url.split("/")[-1]
    dir = "./scripts/{f}".format(f=file_name)

    print("Downloading {scriptName}...".format(scriptName=file_name))

    urllib.request.urlretrieve(url, dir)

def downloadScriptNoOutput(url, dir):
    urllib.request.urlretrieve(url, dir)

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
        binDir = mainDir + "bin"
        scriptsDir = mainDir + "scripts"
        updateDir = mainDir + "update"

        configDir = binDir + "/config.pget"
        hashDir = binDir + "/hash.txt"
    elif whichDir == 2:
        md = mainDir2
        binDir = mainDir2 + "bin"
        scriptsDir = mainDir2 + "scripts"
        updateDir = mainDir2 + "update"

        configDir = binDir + "/config.pget"
        hashDir = binDir + "/hash.txt"

    onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
    localHashFile = open(hashDir, "r+")
    localHash = localHashFile.read()

    if localHash == onlineHash:
        print("There are currently no new updates.")
    else:
        print("There's a new update! Downloading...")
        hashFile = open(hashDir, "w+")
        hashFile.write(requests.get(upgrade_Hash_Location).content.decode("utf8"))

        pgetFile = open(md + "/pget.py", "w+")
        pgetFile.write(requests.get(pget_location).content.decode("utf8"))

        readmeFile = open(md + "/README.md", "w+")
        readmeFile.write(requests.get(readme_location).content.decode("utf8"))

        versionFile = open(binDir + "/version.txt", "w+")
        versionFile.write(requests.get(version_location).content.decode("utf8"))

        updateFile = open(updateDir + "/update.py", "w+")
        updateFile.write(requests.get(upgrade_Script_Location).content.decode("utf8"))

        downloadpyFile = open(binDir + "/download.py", "w+")
        downloadpyFile.write(requests.get(downloadpy_location).content.decode("utf8"))

        print("Succesfully updated PGet!")
else:
    print("Missing hash file. Please redownload from github!")