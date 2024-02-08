from collections import OrderedDict
from intermediate.symtable.SymTableEntry import SymTableEntry


class SymTable(OrderedDict):
    UNNAMED_PREFIX = "_unnamed_"
    unnamedIndex = 0
    serialVersionID = 0

    def __init__(self, nestingLevel):
        super().__init__()
        self.nestingLevel = nestingLevel
        self.slotNumber = -1
        self.maxSlotNumber = 0
        self.ownerId = None

    def getNestingLevel(self):
        return self.nestingLevel

    def getMaxSlotNumber(self):
        return self.maxSlotNumber

    def nextSlotNumber(self):
        self.maxSlotNumber = self.slotNumber = self.slotNumber + 1
        return self.slotNumber

    def getOwner(self):
        return self.ownerId

    def setOwner(self, ownerId):
        self.ownerId = ownerId

    def enter(self, name, kind):
        entry = SymTableEntry(name, kind, self)
        self[name] = entry
        return entry

    def lookup(self, name):
        return self.get(name)

    def sortedEntries(self):
        """Return a list of entries sorted by name."""
        entries = list(self.values())
        entries.sort(key=lambda entry: entry.getName())
        return entries

    def resetVariables(self, kind):
        """Reset all the variable entries to a kind."""
        for entry in self.values():
            if entry.getKind() == kind.VARIABLE:
                entry.setKind(kind)

    @classmethod
    def generateUnnamedName(cls):
        cls.unnamedIndex += 1
        return cls.UNNAMED_PREFIX + str(cls.unnamedIndex)
