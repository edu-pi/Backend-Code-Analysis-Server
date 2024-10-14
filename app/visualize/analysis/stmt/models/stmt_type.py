from utils.enum import Enum


class StmtType(Enum):
    ASSIGN = "assign"
    EXPR = "expr"
    FOR = "for"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    WHILE = "while"

    FUNC_DEF = "func_def"
    USER_FUNC = "user_func"

    FLOW_CONTROL = "flow_control"
    PASS = "pass"
    BREAK = "break"
    CONTINUE = "continue"
