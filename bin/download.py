import urllib.request
from pathlib import Path


class Downloader:
    def downloadFile(self, url, dir):
        file_name = url.split("/")[-1]
        dir = "/{f}".format(f=file_name)

        print("Downloading {scriptName}...".format(scriptName=file_name))

        urllib.request.urlretrieve(url, dir)

    def downloadScript(self, url):
        file_name = url.split("/")[-1]
        dir = "./scripts/{f}".format(f=file_name)

        print("Downloading {scriptName}...".format(scriptName=file_name))

        urllib.request.urlretrieve(url, dir)

    def downloadScriptNoOutput(self, url, dir):
        urllib.request.urlretrieve(url, dir)
