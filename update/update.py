from bin.download import Downloader
from pathlib import Path
import requests

upgrade_Hash_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/bin/hash.txt"
upgrade_Script_Location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/update/update.py"
pget_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/pget.py"
readme_location = "https://raw.githubusercontent.com/Qazaroth/PGet/master/README.md"

mainDir = "././"
binDir = "././bin"
scriptsDir = "././scripts"
updateDir = "././update"
binDir = "././bin"

configDir = binDir + "/config.pget"
hashDir = binDir + "/hash.txt"

print("Checking if there is new update...")
hashFile = Path(hashDir)

if hashFile.is_file():
    onlineHash = requests.get(upgrade_Hash_Location).content.decode("utf8")
    localHashFile = open(hashDir, "r+")
    localHash = localHashFile.read()

    if localHash == onlineHash:
        print("There are currently no new updates.")
    else:
        print("There's a new update! Downloading...")
        Downloader.downloadFile(upgrade_Hash_Location, hashDir)
else:
    print("Hash file missing! Please redownload from github!")