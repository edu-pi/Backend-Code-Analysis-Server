from utils.enum import Enum


class StmtType(Enum):
    ASSIGN = "assign"
    EXPR = "expr"
    FOR = "for"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    WHILE = "while"

    FLOW_CONTROL = "flow_control"
    PASS = "pass"
    BREAK = "break"
    CONTINUE = "continue"
