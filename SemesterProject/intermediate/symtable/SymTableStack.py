from intermediate.symtable.SymTable import SymTable

class SymTableStack(list):
    serialVersionUID = 0

    def __init__(self):
        super().__init__()
        self.programId = None
        self.currentNestingLevel = 0
        self.append(SymTable(self.currentNestingLevel))

    def getCurrentNestingLevel(self):
        return self.currentNestingLevel

    def getProgramId(self):
        return self.programId

    def setProgramId(self, pid):
        self.programId = pid

    def getLocalSymTable(self):
        return self[self.currentNestingLevel]

    def push(self):
        self.currentNestingLevel += 1
        symTable = SymTable(self.currentNestingLevel)
        self.append(symTable)
        return symTable

    def pop(self):
        symTable = self[self.currentNestingLevel]
        # self.remove(self.currentNestingLevel)
        del self[self.currentNestingLevel]
        self.currentNestingLevel -= 1
        return symTable

    def enterLocal(self, name, kind):
        return self[self.currentNestingLevel].enter(name, kind)

    def lookupLocal(self, name):
        return self[self.currentNestingLevel].lookup(name)

    def lookup(self, name):
        for i in range(self.currentNestingLevel, -1, -1):
            entry = self[i].lookup(name)
            if entry:
                return entry
        progID = self.programId.name.lower()
        if name == progID:
            return self.programId
        return None
