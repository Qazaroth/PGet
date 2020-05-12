from pathlib import  Path
from bin import download

url = "https://raw.githubusercontent.com/Qazaroth/pget-list/master/test.py"

file_name = url.split("/")[-1]
dir = "./scripts/{f}".format(f=file_name)

f = Path(dir)

print("Beginning file download...")

download.Downloader.downloadScript(url)