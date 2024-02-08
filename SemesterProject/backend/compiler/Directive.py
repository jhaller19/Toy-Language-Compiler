from enum import Enum


class Directive(Enum):
    CLASS_PUBLIC = ".class public"
    END_CLASS = ".end class"
    SUPER = ".super"
    FIELD = ".field"
    FIELD_PRIVATE_STATIC = ".field private static"
    METHOD_PUBLIC = ".method public"
    METHOD_STATIC = ".method static"
    METHOD_PUBLIC_STATIC = ".method public static"
    METHOD_PRIVATE_STATIC = ".method private static"
    END_METHOD = ".end method"
    LIMIT_LOCALS = ".limit locals"
    LIMIT_STACK = ".limit stack"
    VAR = ".var"
    LINE = ".line"

    def __str__(self):
        return self.value
