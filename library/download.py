import requests


def downloadFile(url, dirOfFile, silent=False):
    file_name = url.split("/")[-1]

    if not silent or not bool(silent):
        print("Downloading {scriptName}...".format(scriptName=file_name))

    with open(dirOfFile, "w+") as f:
        f.write(requests.get(url).content.decode("utf8"))
