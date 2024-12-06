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
    LEN = "len"

    # attribute
    APPEND = "append"
    REMOVE = "remove"
    EXTEND = "extend"
    POP = "pop"
    INSERT = "insert"

    # function
    FUNC = "function"
    USER_FUNC = "user_function"

    @staticmethod
    def judge_collection_type(value):
        if isinstance(value, str):
            try:
                value = eval(value)
                ExprType.judge_collection_type(value)
            except (SyntaxError, NameError):
                value = value  # 그냥 문자열이 들어오는 경우

        if isinstance(value, list):
            return ExprType.LIST

        elif isinstance(value, tuple):
            return ExprType.TUPLE

        elif isinstance(value, dict):
            return ExprType.DICT

        return ExprType.VARIABLE
