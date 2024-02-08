from enum import Enum


class BackendMode(Enum):
    EXECUTOR = 1
    CONVERTER = 2
    COMPILER = 3