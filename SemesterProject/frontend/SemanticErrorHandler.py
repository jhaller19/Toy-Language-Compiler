from enum import Enum


class SemanticErrorHandler:

    def __init__(self):
        self.count = 0

    def getCount(self):
        return self.count

    def flag(self, code, lineNumber, text):
        print("SEMANTIC ERROR: ", code.value, " at line ", lineNumber, " near ", text)
        self.count += 1

    def flagCtx(self, code, ctx):
        self.flag(code, ctx.start.line, ctx.getText())


class Code(Enum):
    UNDECLARED_IDENTIFIER = "Undeclared identifier"
    REDECLARED_IDENTIFIER = "Redeclared identifier"
    INVALID_CONSTANT = "Invalid constant"
    INVALID_OPERATOR = "Invalid operator"
    INVALID_SIGN = "Invalid sign"
    INVALID_TYPE = "Invalid type"
    INVALID_VARIABLE = "Invalid variable"
    TYPE_MISMATCH = "Type mismatch"
    TYPE_MUST_BE_INTEGER = "Datatype must be integer"
    TYPE_MUST_BE_NUMERIC = "Datatype must be integer or real"
    TYPE_MUST_BE_BOOLEAN = "Datatype must be boolean"
    TYPE_MUST_BE_STRING = "Datatype must be string"
    INCOMPATIBLE_ASSIGNMENT = "Incompatible assignment"
    INCOMPATIBLE_COMPARISON = "Incompatible comparison"
    DUPLICATE_CASE_CONSTANT = "Duplicate CASE constant"
    INVALID_CONTROL_VARIABLE = "Invalid control variable datatype"
    NAME_MUST_BE_PROCEDURE = "Must be a procedure name"
    NAME_MUST_BE_FUNCTION = "Must be a function name"
    ARGUMENT_COUNT_MISMATCH = "Invalid number of arguments"
    ARGUMENT_MUST_BE_VARIABLE = "Argument must be a variable"
    INVALID_REFERENCE_PARAMETER = "Reference parameter cannot be scalar"
    INVALID_RETURN_TYPE = "Invalid function return type"
    TOO_MANY_SUBSCRIPTS = "Too many subscripts"
    INVALID_FIELD = "Invalid field"

