class Command:
    def __init__(self, cmdName, cmdDescription) -> None:
        self._name = cmdName
        self._desc = cmdDescription

    def getName(self):
        return self._name

    def getDescription(self):
        return self._desc

    def run(self) -> None:
        pass

    def getUsage(self):
        pass

    def getInfo(self):
        return "Default command information. Specify arguments and etcetra here."
