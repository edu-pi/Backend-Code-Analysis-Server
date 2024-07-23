from enum import Enum


class ExprType(Enum):
    # expr
    NAME = "name"
    VARIABLE = "variable"
    LIST = "list"
    TUPLE = "tuple"

    # compare
    COMPARE = "compare"

    # array slice
    SUBSCRIPT = "subscript"
    SLICE = "slice"

    # call
    CALL = "call"
    RANGE = "range"
    PRINT = "print"

    # attribute
    APPEND = "append"

    @staticmethod
    def get_type(value):
        if isinstance(value, list):
            return ExprType.LIST

        elif isinstance(value, tuple):
            return ExprType.TUPLE

        return ExprType.VARIABLE
