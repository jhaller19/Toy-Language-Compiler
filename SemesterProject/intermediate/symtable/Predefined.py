from .Routine import Routine
from .Kind import Kind
from ..type.Typespec import Typespec
from ..type.Typespec import Form


class Predefined:
    # Predefined types.
    integerType = None
    realType = None
    booleanType = None
    charType = None
    stringType = None
    undefinedType = None

    # Predefined identifiers.
    integerId = None
    realId = None
    booleanId = None
    charId = None
    stringId = None
    falseId = None
    trueId = None
    readId = None
    readlnId = None
    writeId = None
    writelnId = None
    absId = None
    arctanId = None
    chrId = None
    cosId = None
    eofId = None
    eolnId = None
    expId = None
    lnId = None
    oddId = None
    ordId = None
    predId = None
    roundId = None
    sinId = None
    sqrId = None
    sqrtId = None
    succId = None
    truncId = None

    @classmethod
    def initialize(cls, symTableStack):
        cls.initializeTypes(symTableStack)
        cls.initializeConstants(symTableStack)
        cls.initializeStandardRoutines(symTableStack)

    @classmethod
    def initializeTypes(cls, symTableStack):
        cls.integerId = symTableStack.enterLocal("integer", Kind.TYPE)
        cls.integerType = Typespec(Form.SCALAR)
        cls.integerType.setIdentifier(cls.integerId)
        cls.integerId.setType(cls.integerType)

        cls.realId = symTableStack.enterLocal("real", Kind.TYPE)
        cls.realType = Typespec(Form.SCALAR)
        cls.realType.setIdentifier(cls.realId)
        cls.realId.setType(cls.realType)

        cls.booleanId = symTableStack.enterLocal("boolean", Kind.TYPE)
        cls.booleanType = Typespec(Form.ENUMERATION)
        cls.booleanType.setIdentifier(cls.booleanId)
        cls.booleanId.setType(cls.booleanType)

        cls.charId = symTableStack.enterLocal("char", Kind.TYPE)
        cls.charType = Typespec(Form.SCALAR)
        cls.charType.setIdentifier(cls.charId)
        cls.charId.setType(cls.charType)

        cls.stringId = symTableStack.enterLocal("string", Kind.TYPE)
        cls.stringType = Typespec(Form.SCALAR)
        cls.stringType.setIdentifier(cls.stringId)
        cls.stringId.setType(cls.stringType)

        cls.undefinedType = Typespec(Form.SCALAR)

    @classmethod
    def initializeConstants(cls, symTableStack):
        cls.falseId = symTableStack.enterLocal("false", Kind.ENUMERATION_CONSTANT)
        cls.falseId.setType(cls.booleanType)
        cls.falseId.setValue(0)

        cls.trueId = symTableStack.enterLocal("true", Kind.ENUMERATION_CONSTANT)
        cls.trueId.setType(cls.booleanType)
        cls.trueId.setValue(1)

        constants = cls.booleanType.getEnumerationConstants()
        constants.append(cls.falseId)
        constants.append(cls.trueId)

    @classmethod
    def initializeStandardRoutines(cls, symTableStack):
        cls.readId = cls.enterStandard(symTableStack, Kind.PROCEDURE, "read", Routine.READ)
        cls.readlnId = cls.enterStandard(symTableStack, Kind.PROCEDURE, "readln", Routine.READLN)
        cls.writeId = cls.enterStandard(symTableStack, Kind.PROCEDURE, "write", Routine.WRITE)
        cls.writelnId = cls.enterStandard(symTableStack, Kind.PROCEDURE, "writeln", Routine.WRITELN)
        cls.absId = cls.enterStandard(symTableStack, Kind.FUNCTION, "abs", Routine.ABS)
        cls.arctanId = cls.enterStandard(symTableStack, Kind.FUNCTION, "arctan", Routine.ARCTAN)
        cls.chrId = cls.enterStandard(symTableStack, Kind.FUNCTION, "chr", Routine.CHR)
        cls.cosId = cls.enterStandard(symTableStack, Kind.FUNCTION, "cos", Routine.COS)
        cls.eofId = cls.enterStandard(symTableStack, Kind.FUNCTION, "eof", Routine.EOF)
        cls.eolnId = cls.enterStandard(symTableStack, Kind.FUNCTION, "eoln", Routine.EOLN)
        cls.expId = cls.enterStandard(symTableStack, Kind.FUNCTION, "exp", Routine.EXP)
        cls.lnId = cls.enterStandard(symTableStack, Kind.FUNCTION, "ln", Routine.LN)
        cls.oddId = cls.enterStandard(symTableStack, Kind.FUNCTION, "odd", Routine.ODD)
        cls.ordId = cls.enterStandard(symTableStack, Kind.FUNCTION, "ord", Routine.ORD)
        cls.predId = cls.enterStandard(symTableStack, Kind.FUNCTION, "pred", Routine.PRED)
        cls.roundId = cls.enterStandard(symTableStack, Kind.FUNCTION, "round", Routine.ROUND)
        cls.sinId = cls.enterStandard(symTableStack, Kind.FUNCTION, "sin", Routine.SIN)
        cls.sqrId = cls.enterStandard(symTableStack, Kind.FUNCTION, "sqr", Routine.SQR)
        cls.sqrtId = cls.enterStandard(symTableStack, Kind.FUNCTION, "sqrt", Routine.SQRT)
        cls.succId = cls.enterStandard(symTableStack, Kind.FUNCTION, "succ", Routine.SUCC)
        cls.truncId = cls.enterStandard(symTableStack, Kind.FUNCTION, "trunc", Routine.TRUNC)

    @classmethod
    def enterStandard(cls, symTableStack, kind, name, routineCode):
        routineId = symTableStack.enterLocal(name, kind)
        routineId.setRoutineCode(routineCode)
        return routineId
