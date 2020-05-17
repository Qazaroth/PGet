import requests


class Downloader:
    @staticmethod
    def downloadScriptNoOutput(self, url, dirOfFile):
        f = open(dirOfFile, "w+")
        f.write(requests.get(url).content.decode("utf8"))

    @staticmethod
    def downloadFile(self, url, dirOfFile):
        file_name = url.split("/")[-1]
        dirOfFile = dirOfFile + "/{f}".format(f=file_name)

        print("Downloading {scriptName}...".format(scriptName=file_name))

        Downloader.downloadScriptNoOutput(self, url, dirOfFile)

    @staticmethod
    def downloadFileSilent(self, url, dirOfFile):
        file_name = url.split("/")[-1]
        dirOfFile = dirOfFile + "/{f}".format(f=file_name)

        Downloader.downloadScriptNoOutput(self, url, dirOfFile)
