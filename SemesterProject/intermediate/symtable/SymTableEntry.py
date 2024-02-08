from intermediate.symtable.Kind import Kind


class SymTableEntry:
    def __init__(self, name, kind, symTable):
        self.name = name
        self.symtable = symTable
        self.lineNumbers = []
        self.kind = kind
        self.typespec = None
        self.slotNumber = None
        self.info = None
        match kind:
            case Kind.CONSTANT | Kind.ENUMERATION_CONSTANT | Kind.VARIABLE | Kind.RECORD_FIELD | Kind.VALUE_PARAMETER:
                self.info = ValueInfo()
            case Kind.CLASS | Kind.PROCEDURE | Kind.FUNCTION:
                self.info = RoutineInfo()
                self.info.parameters = []
                self.info.subroutines = []
            case _:
                pass

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getKind(self):
        return self.kind

    def setKind(self, kind):
        self.kind = kind

    def getSymtable(self):
        return self.symtable

    def setSymtable(self, symtable):
        self.symtable = symtable

    def getSlotNumber(self):
        return self.slotNumber

    def setSlotNumber(self, slotNumber):
        self.slotNumber = slotNumber

    def getType(self):
        return self.typespec

    def setType(self, typespec):
        self.typespec = typespec

    def getLineNumbers(self):
        return self.lineNumbers

    def appendLineNumber(self, lineNumber):
        self.lineNumbers.append(lineNumber)

    def getValue(self):
        return self.info.value

    def setValue(self, value):
        self.info.value = value

    def getRoutineCode(self):
        return self.info.code

    def setRoutineCode(self, code):
        self.info.code = code

    def getRoutineSymtable(self):
        return self.info.symTable

    def setRoutineSymtable(self, symTable):
        self.info.symTable = symTable

    def getRoutineParameters(self):
        return self.info.parameters

    def setRoutineParameters(self, parameters):
        self.info.parameters = parameters

    def getSubroutines(self):
        return self.info.subroutines

    def appendSubroutine(self, subroutineId):
        self.info.subroutines.append(subroutineId)

    def getExecutable(self):
        return self.info.executable

    def setExecutable(self, executable):
        self.info.executable = executable


class EntryInfo:
    pass


class ValueInfo(EntryInfo):
    def __init__(self):
        self.value = None


class RoutineInfo(EntryInfo):
    def __init__(self):
        self.code = None
        self.symTable = None
        self.parameters = None
        self.subroutines = None
        self.executable = None
