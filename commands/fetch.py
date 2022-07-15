from commands import Command
from scriptFunctions import downloadFile, settings
from pathlib import Path

import os, requests

def fetchScript(args):
    argsArray = args.split("\"")
    inpScriptName = argsArray[0]

    scriptListFile = Path(settings.scriptListDir)

    if scriptListFile.is_file():
        scriptListFile = open(settings.scriptListDir, "r")
        scriptListFileContent = scriptListFile.read()
        listFileContents = scriptListFileContent.split("--")
        listFileContents.pop(0)

        for i in listFileContents:
            scriptDetails = i.split(",")
            scriptName = scriptDetails[1]
            scriptURL = scriptDetails[2]
            scriptHash = scriptDetails[5]
            scriptAuthor = scriptDetails[6]
            scriptCategory = scriptDetails[7]

            catDir = "./scripts/{c}".format(c=scriptCategory)
            catDir = Path(catDir)

            if catDir.is_dir():
                if inpScriptName == scriptName:
                    file_name = scriptURL.split("/")[-1]
                    dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                    hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                    batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName, f=scriptName)

                    scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                    tmpFile = Path(scriptDir)

                    if not tmpFile.is_dir():
                        print("Downloading \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m...".format(f=file_name,
                                                                                                   a=scriptAuthor)
                              )
                        os.mkdir(scriptDir)
                        downloadFile(scriptURL, dir, True)
                        tmpFile = open(hashScriptDir, "w+")
                        tmpFile.write(scriptHash)
                        tmpFile = open(batScriptDir, "w+")
                        tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                              a=scriptAuthor,
                                                                                              f=file_name))
                        print("Downloaded \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m.".format(f=file_name,
                                                                                                a=scriptAuthor))
                        tmpFile.close()
                    else:
                        print("\033[1;2;32m{f}\033[m already exists..".format(f=scriptName))
                    break
            else:
                if inpScriptName == scriptName:
                    os.mkdir(catDir)
                    file_name = scriptURL.split("/")[-1]
                    dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                    hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                    batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName, f=scriptName)

                    scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                    tmpFile = Path(scriptDir)

                    if not tmpFile.is_dir():
                        print("Downloading \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m...".format(f=file_name,
                                                                                                   a=scriptAuthor)
                              )
                        os.mkdir(scriptDir)
                        downloadFile(scriptURL, dir, True)
                        tmpFile = open(hashScriptDir, "w+")
                        tmpFile.write(scriptHash)
                        tmpFile = open(batScriptDir, "w+")
                        tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                              a=scriptAuthor,
                                                                                              f=file_name))
                        print("Downloaded \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m.".format(f=file_name,
                                                                                                a=scriptAuthor))
                        tmpFile.close()
                    else:
                        print("\033[1;2;32m{f}\033[m already exists..".format(f=scriptName))
                    tmpFile.close()
                    break
        scriptListFile.close()
    else:
        tmpFileContent = requests.get(settings.script_List_Location).content.decode("utf8")

        tmpFileContentArray = tmpFileContent.split("--")
        tmpFileContentArray.pop(0)

        for i in tmpFileContentArray:
            scriptDetails = i.split(",")
            scriptDetails.pop(0)

            scriptName = scriptDetails[0]
            scriptURL = scriptDetails[1]
            scriptDesc = scriptDetails[2]
            scriptFileName = scriptDetails[3]
            scriptHash = scriptDetails[4]
            scriptAuthor = scriptDetails[5]
            scriptCategory = scriptDetails[6]

            if inpScriptName == scriptName:
                catDir = "./scripts/{c}".format(c=scriptCategory)
                catDir = Path(catDir)

                if catDir.is_dir():
                    if inpScriptName == scriptName:
                        file_name = scriptURL.split("/")[-1]
                        dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                        hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                        batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName,
                                                                          f=scriptName)

                        scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                        tmpFile = Path(scriptDir)

                        if not tmpFile.is_dir():
                            print("Downloading \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m...".format(
                                f=file_name,
                                a=scriptAuthor)
                            )
                            os.mkdir(scriptDir)
                            downloadFile(scriptURL, dir, True)
                            tmpFile = open(hashScriptDir, "w+")
                            tmpFile.write(scriptHash)
                            tmpFile = open(batScriptDir, "w+")
                            tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                  a=scriptAuthor,
                                                                                                  f=file_name))
                            print("Downloaded \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m.".format(f=file_name,
                                                                                                    a=scriptAuthor))
                            tmpFile.close()
                        else:
                            print("\033[1;2;32m{f}\033[m already exists..".format(f=scriptName))
                        break
                else:
                    os.mkdir(catDir)

                    if inpScriptName == scriptName:
                        file_name = scriptURL.split("/")[-1]
                        dir = "./scripts/{c}/{s}/{f}".format(s=scriptName, f=file_name, c=scriptCategory)
                        hashScriptDir = "./scripts/{c}/{s}/hash.txt".format(s=scriptName, c=scriptCategory)
                        batScriptDir = "./scripts/{c}/{s}/{f}.bat".format(c=scriptCategory, s=scriptName,
                                                                          f=scriptName)

                        scriptDir = "./scripts/{c}/{s}".format(s=scriptName, c=scriptCategory)

                        tmpFile = Path(scriptDir)

                        if not tmpFile.is_dir():
                            print("Downloading \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m...".format(f=file_name,
                                                                                                       a=scriptAuthor)
                                  )
                            os.mkdir(scriptDir)
                            downloadFile(scriptURL, dir, True)
                            tmpFile = open(hashScriptDir, "w+")
                            tmpFile.write(scriptHash)
                            tmpFile = open(batScriptDir, "w+")
                            tmpFile.write("@echo off\ntitle {s} by {a}\npython {f}\npause".format(s=scriptName,
                                                                                                  a=scriptAuthor,
                                                                                                  f=file_name))
                            print("Downloaded \033[1;2;32m{f}\033[m by \033[1;37m{a}\033[m.".format(f=file_name,
                                                                                                    a=scriptAuthor))
                            tmpFile.close()
                        else:
                            print("\033[1;2;32m{f}\033[m already exists..".format(f=scriptName))
                        break

class FetchCMD(Command.Command):
    def __init__(self) -> None:
        super().__init__("fetch", "Fetches/Downloads the specified script from the \"server\".")

    def run(self, args):
        fetchScript(args)

    def getUsage(self):
        return "\033[1mfetch\033[m <\033[31mSCRIPT_NAME\033[m>"

    def getInfo(self):
        return "Usage: \033[1mfetch\033[m <\033[31mSCRIPT_NAME\033[m>\nExample: fetch test"

    
