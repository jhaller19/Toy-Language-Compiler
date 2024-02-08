from .Typespec import Form
from ..symtable.Predefined import Predefined


class TypeChecker:
    @staticmethod
    def isInteger(type):
        return type is not None and type.baseType() is Predefined.integerType

    @staticmethod
    def areBothInteger(type1, type2):
        return TypeChecker.isInteger(type1) and TypeChecker.isInteger(type2)

    @staticmethod
    def isReal(type):
        return type is not None and type.baseType() is Predefined.realType

    @staticmethod
    def areBothReal(type1, type2):
        return TypeChecker.isReal(type1) and TypeChecker.isReal(type2)

    @staticmethod
    def isIntegerOrReal(type):
        return TypeChecker.isInteger(type) or TypeChecker.isReal(type)

    @staticmethod
    def isAtLeastOneReal(type1, type2):
        return (TypeChecker.isReal(type1) and TypeChecker.isReal(type2)) or \
            (TypeChecker.isReal(type1) and TypeChecker.isInteger(type2)) or \
            (TypeChecker.isInteger(type1) and TypeChecker.isReal(type2))

    @staticmethod
    def isBoolean(type):
        return type is not None and type.baseType() is Predefined.booleanType

    @staticmethod
    def areBothBoolean(type1, type2):
        return TypeChecker.isBoolean(type1) and TypeChecker.isBoolean(type2)

    @staticmethod
    def isChar(type):
        return type is not None and type.baseType() is Predefined.charType

    @staticmethod
    def isString(type):
        return type is not None and type.baseType() is Predefined.stringType

    @staticmethod
    def areBothString(type1, type2):
        return TypeChecker.isString(type1) and TypeChecker.isString(type2)

    @staticmethod
    def areAssignmentCompatible(targetType, valueType):
        if targetType is None or valueType is None:
            return False

        targetType = targetType.baseType()
        valueType = valueType.baseType()

        compatible = False

        # Identical types.
        if targetType == valueType:
            compatible = True

        # real := integer
        elif TypeChecker.isReal(targetType) and TypeChecker.isInteger(valueType):
            compatible = True

        if valueType.getForm() == Form.ITERATOR:
            compatible = True

        return compatible

    @staticmethod
    def areComparisonCompatible(type1, type2):
        if type1 is None or type2 is None:
            return False

        type1 = type1.baseType()
        type2 = type2.baseType()
        form = type1.getForm()

        compatible = False

        # Two identical scalar or enumeration types.
        if type1 == type2 and (form == Form.SCALAR or form == Form.ENUMERATION):
            compatible = True

        # One integer and one real.
        elif TypeChecker.isAtLeastOneReal(type1, type2):
            compatible = True

        return compatible
