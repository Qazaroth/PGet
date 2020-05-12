from pathlib import Path
from bin.download import Downloader

binDir = "./bin"
scriptsDir = "./scripts"

configDir = "{b}/config.pget".format(b=binDir)
hashDir = "{b}/hash.txt".format(b=binDir)

def init():
    hashFile = Path(hashDir)

    if hashFile.is_file():
        print("Checking if config.pget exists...")
        configFile = Path(configDir)

        if not configFile.is_file():
            print("config.pget does not exist... making one...")
            configFile = open(configDir, "w+")
            configFile.write("[DO NOT DELETE]")
            print("Made config.pget. Do not delete this file!")
        else:
            print("config.pget exist! Do not delete this file!")
    else:
        print("Please get PGet from Github...")


def main():
    init()


main()

# url = "https://raw.githubusercontent.com/Qazaroth/pget-list/master/test.py"

# file_name = url.split("/")[-1]
# dir = "{s}/{f}".format(s=scriptsDir, f=file_name)

# f = Path(dir)

# print("Beginning file download...")

# Downloader.downloadScript(url)
