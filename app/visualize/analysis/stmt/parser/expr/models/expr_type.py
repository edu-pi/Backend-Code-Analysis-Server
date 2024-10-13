from enum import Enum


class ExprType(Enum):
    # expr
    NAME = "name"
    VARIABLE = "variable"
    LIST = "list"
    TUPLE = "tuple"
    DICT = "dict"

    # compare
    COMPARE = "compare"

    # array slice
    SUBSCRIPT = "subscript"
    SLICE = "slice"

    # call
    CALL = "call"
    RANGE = "range"
    PRINT = "print"
    INPUT = "input"

    # attribute
    APPEND = "append"
    REMOVE = "remove"
    EXTEND = "extend"
    POP = "pop"
    INSERT = "insert"

    # function
    FUNC = "function"

    @staticmethod
    def judge_collection_type(value):
        if isinstance(value, str):
            try:
                value = eval(value)
            except (SyntaxError, NameError):
                return ExprType.VARIABLE

        if isinstance(value, list):
            return ExprType.LIST

        elif isinstance(value, tuple):
            return ExprType.TUPLE

        elif isinstance(value, dict):
            return ExprType.DICT

        return ExprType.VARIABLE
