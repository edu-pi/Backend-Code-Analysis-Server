from enum import Enum


class VizType(Enum):
    ASSIGN_VIZ = "assign"
    EXPR_VIZ = "expr"
    FOR_VIZ = "for"

    IF_ELSE_DEFINE = "ifElseDefine"
    IF_ELSE_CHANGE = "ifElseChange"

    APPEND_VIZ = "append"
