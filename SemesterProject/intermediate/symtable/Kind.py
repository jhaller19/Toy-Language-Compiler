from enum import Enum


class Kind(Enum):
    CONSTANT = 1
    ENUMERATION_CONSTANT = 2
    TYPE = 3
    VARIABLE = 4
    RECORD_FIELD = 5
    VALUE_PARAMETER = 6
    REFERENCE_PARAMETER = 7
    PROGRAM_PARAMETER = 8
    CLASS = 9 #was program
    PROCEDURE = 10
    FUNCTION = 11
    UNDEFINED = 12

    def __str__(self):
        return self.name.lower()
