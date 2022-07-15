# import Command

class CommandHandler:
    def __init__(self) -> None:
        self.__commands = {}
        self.__alias = {}

    def addCommand(self, name, cmd):
        k = self.__commands.get(name, None)
        if k is None:
            self.__commands[name] = cmd

    def getCommands(self):
        return self.__commands

    def getCommand(self, name):
        return self.__commands.get(name, None)

    def getAliases(self, name):
        return self.__alias.get(name, None)

    def addAlias(self, name, alias):
        k : list = self.__alias.get(name, [])
        if k.count <= 0:
            self.__alias[name] = [alias]
        else:
            v = k.append(alias)
            self.__alias[name] = v