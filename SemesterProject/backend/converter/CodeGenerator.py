class CodeGenerator:
    blanks = "          " * 8

    def __init__(self, objectFile):
        self.objectFile = objectFile
        self.length = 0
        self.position = 0
        self.indentation = ""
        self.needLF = False


    def close(self):
        self.objectFile.close()

    def lfIfNeeded(self):
        if self.needLF:
            self.objectFile.write("\n")
            self.objectFile.flush()
            self.length = 0
            self.needLF = False

    def emit(self, code):
        self.objectFile.write(code)
        self.objectFile.flush()
        self.length += len(code)
        self.needLF = True

    def emitStart(self):
        self.lfIfNeeded()
        self.emit(self.indentation)
        self.position = 0

    def emitStartCode(self, code=None):
        self.lfIfNeeded()
        self.emit(self.indentation + code)
        self.position = 0

    def emitLineCode(self, code=None):
        self.lfIfNeeded()
        self.objectFile.write(self.indentation + code + "\n")
        self.objectFile.flush()
        self.length = 0
        self.position = 0
        self.needLF = False

    def emitLine(self):
        self.lfIfNeeded()
        self.objectFile.write("\n")
        self.objectFile.flush()
        self.length = 0
        self.position = 0
        self.needLF = False

    def emitEnd(self, code=None):
        self.objectFile.write(code + "\n")
        self.objectFile.flush()
        self.length = 0
        self.position = 0
        self.needLF = False

    def indent(self):
        self.indentation += "    "

    def dedent(self):
        self.indentation = self.indentation[:-4]

    def emitCommentLine(self, text=None):
        self.emitLineCode(self.indentation + "// " + text)
        self.needLF = False

    def mark(self):
        self.position = self.length

    def split(self, limit):
        if self.position > limit:
            self.objectFile.write("\n")
            self.objectFile.write(self.blanks[:self.position])
            self.objectFile.flush()

            self.length = self.position
            self.position = 0
            self.needLF = False