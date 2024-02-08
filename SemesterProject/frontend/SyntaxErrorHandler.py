class SyntaxErrorHandler:
    count = 0
    first = True

    def __init__(self):
        pass

    def getCount(self):
        return self.count

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, ex):
        if self.first:
            print("\n\n===== SYNTAX ERRORS =====\n")
            print("%-4s %-35s" % ("Line", "Message"))
            print("%-4s %-35s" % ("----", "-------"))
            self.first = False
        self.count += 1
        print("%03d  %-35s" % (line, msg))
