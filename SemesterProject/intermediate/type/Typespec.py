from enum import Enum


class Typespec:

    def __init__(self, form):
        self.form = form
        self.identifier = None
        if form == Form.ENUMERATION:
            self.info = EnumerationInfo()
            self.info.constants = []
        elif form == Form.SUBRANGE:
            self.info = SubrangeInfo()
            self.info.minValue = 0
            self.info.maxValue = 0
            self.info.baseType = None
        elif form == Form.ARRAY or form == Form.ITERATOR:
            self.info = ArrayInfo()
            self.info.indexType = None
            self.info.elementType = None
            self.info.elementCount = 0
        elif form == Form.RECORD:
            self.info = RecordInfo()
            self.info.typePath = None
            self.info.symTable = None


    def isStructured(self):
        return self.form == Form.ARRAY or self.form == Form.RECORD

    def getForm(self):
        return self.form

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def baseType(self):
        return self.info.baseType if self.form == Form.SUBRANGE else self

    def getSubrangeBaseType(self):
        return self.info.baseType

    def setSubrangeBaseType(self, baseType):
        self.info.baseType = baseType

    def getSubrangeMinValue(self):
        return self.info.minValue

    def setSubrangeMinValue(self, minValue):
        self.info.minValue = minValue

    def getSubrangeMaxValue(self):
        return self.info.maxValue

    def setSubrangeMaxValue(self, maxValue):
        self.info.maxValue = maxValue

    def getEnumerationConstants(self):
        return self.info.constants

    def setEnumerationConstants(self, constants):
        self.info.constants = constants

    def getArrayIndexType(self):
        return self.info.indexType

    def setArrayIndexType(self, indexType):
        self.info.indexType = indexType

    def getArrayElementType(self):
        return self.info.elementType

    def setArrayElementType(self, elementType):
        self.info.elementType = elementType

    def getArrayElementCount(self):
        return self.info.elementCount

    def setArrayElementCount(self, elementCount):
        self.info.elementCount = elementCount

    def getArrayBaseType(self):
        elemType = self
        while elemType.form == Form.ARRAY:
            elemType = elemType.info.elementType
        return elemType.baseType()

    def getRecordSymTable(self):
        return self.info.symTable

    def setRecordSymTable(self, symTable):
        self.info.symTable = symTable

    def getRecordTypePath(self):
        return self.info.typePath

    def setRecordTypePath(self, typePath):
        self.info.typePath = typePath


class Form(Enum):
    SCALAR = 1
    ENUMERATION = 2
    SUBRANGE = 3
    ARRAY = 4
    RECORD = 5
    UNKNOWN = 6
    ITERATOR = 7

    def __str__(self):
        return self.name.lower()


class TypeInfo:
    pass


class EnumerationInfo(TypeInfo):
    def __init__(self):
        self.constants = None


class SubrangeInfo(TypeInfo):
    def __init__(self):
        self.minValue = None
        self.maxValue = None
        self.baseType = None


class ArrayInfo(TypeInfo):
    def __init__(self):
        self.indexType = None
        self.elementType = None
        self.elementCount = None


class RecordInfo(TypeInfo):
    def __init__(self):
        self.typePath = None
        self.symTable = None
