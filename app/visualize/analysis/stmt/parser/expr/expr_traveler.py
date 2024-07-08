import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.parser.binop_expr import BinopExpr
from app.visualize.analysis.stmt.parser.expr.parser.call_expr import CallExpr
from app.visualize.analysis.stmt.parser.expr.parser.compare_expr import CompareExpr
from app.visualize.analysis.stmt.parser.expr.parser.constant_expr import ConstantExpr
from app.visualize.analysis.stmt.parser.expr.parser.list_expr import ListExpr
from app.visualize.analysis.stmt.parser.expr.parser.name_expr import NameExpr


class ExprTraveler:

    @staticmethod
    def travel(node: ast, elem_container: ElementContainer):
        if isinstance(node, ast.BinOp):
            return ExprTraveler._binop_travel(node, elem_container)

        elif isinstance(node, ast.Name):
            return ExprTraveler._name_travel(node, elem_container)

        elif isinstance(node, ast.Constant):
            return ExprTraveler._constant_travel(node)

        elif isinstance(node, ast.Call):
            return ExprTraveler._call_travel(node, elem_container)

        elif isinstance(node, ast.List):
            return ExprTraveler._list_travel(node, elem_container)

        elif isinstance(node, ast.Compare):
            compare_obj = ExprTraveler._compare_travel(node, elem_container)
            return compare_obj

        else:
            raise TypeError(f"[ExprTraveler] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _binop_travel(node: ast, elem_container: ElementContainer):
        if isinstance(node, ast.BinOp):
            left = ExprTraveler._binop_travel(node.left, elem_container)
            right = ExprTraveler._binop_travel(node.right, elem_container)
            op = node.op
            return BinopExpr.parse(left, right, op)

        elif isinstance(node, ast.Name):
            return ExprTraveler._name_travel(node, elem_container)

        elif isinstance(node, ast.Constant):
            return ExprTraveler._constant_travel(node)

        else:
            raise TypeError(f"[ExprTraveler - binop parsing 중  {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _name_travel(node: ast.Name, elem_container: ElementContainer):
        return NameExpr.parse(node.ctx, node.id, elem_container)

    @staticmethod
    def _constant_travel(node: ast.Constant):
        return ConstantExpr.parse(node)

    @staticmethod
    def _call_travel(node: ast.Call, elem_container: ElementContainer):
        func_name = ExprTraveler._get_func_name(node.func)
        args = [ExprTraveler.travel(arg, elem_container) for arg in node.args]
        keyword_dict = {
            keyword.arg: ExprTraveler.travel(keyword.value, elem_container).value for keyword in node.keywords
        }

        return CallExpr.parse(func_name, args, keyword_dict)

    @staticmethod
    def _list_travel(node: ast.List, elem_container: ElementContainer):
        elts = [ExprTraveler.travel(elt, elem_container) for elt in node.elts]
        return ListExpr.parse(elts)

    @staticmethod
    def _compare_travel(node: ast.Compare, elem_container: ElementContainer):
        if isinstance(node, ast.Compare):
            left = ExprTraveler._compare_travel(node.left, elem_container)
            comparators = tuple(ExprTraveler._compare_travel(comparor, elem_container) for comparor in node.comparators)

            return CompareExpr.parse(left, tuple(comparators), tuple(node.ops))

        elif isinstance(node, ast.BinOp):
            return ExprTraveler.travel(node, elem_container)

        elif isinstance(node, ast.Name):
            return ExprTraveler.travel(node, elem_container)

        elif isinstance(node, ast.Constant):
            return ExprTraveler.travel(node, elem_container)

        else:
            raise TypeError(f"[ExprTraveler - compare parsing 중  {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _get_func_name(node: ast):
        if isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Attribute):
            raise NotImplementedError(f"[call_travel] {type(node)}정의되지 않았습니다.")

        else:
            raise TypeError(f"[call_travel] {type(node)}는 잘못된 타입입니다.")
