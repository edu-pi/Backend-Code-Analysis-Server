import ast

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.func_def_stmt_obj import FuncDetails, FuncDefStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.container.element_container import ElementContainer


class FuncDefStmt:

    @staticmethod
    def parse(node: ast.FunctionDef, elem_container: ElementContainer):
        name = node.name
        arguments_obj = ExprTraveler.travel(node.args, elem_container)
        body = node.body

        details = FuncDetails(args=arguments_obj.value, body=body)
        elem_container.set_element(name, details)

        expr_stmt_obj = ExprStmtObj(
            id=node.lineno,
            expressions=FuncDefStmt.makeExpressions(name, arguments_obj.value),
            value=name,
            expr_type=ExprType.FUNC,
        )
        return FuncDefStmtObj(target=name, expr_stmt_obj=expr_stmt_obj)

    @staticmethod
    def makeExpressions(name, args) -> tuple:
        return (f"{name}({', '.join(args)})",)
