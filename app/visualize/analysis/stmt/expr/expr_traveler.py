import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.parser.binop_expr import BinopExpr
from app.visualize.analysis.stmt.expr.parser.call_expr import CallExpr
from app.visualize.analysis.stmt.expr.parser.constant_expr import ConstantExpr
from app.visualize.analysis.stmt.expr.parser.name_expr import NameExpr


class ExprTraveler:

    @staticmethod
    def binop_travel(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.BinOp):
            left = ExprTraveler.binop_travel(node.left, elem_manager)
            right = ExprTraveler.binop_travel(node.right, elem_manager)
            op = node.op
            return BinopExpr.parse(left, right, op, elem_manager)

        elif isinstance(node, ast.Name):
            return ExprTraveler.name_travel(node, elem_manager)

        elif isinstance(node, ast.Constant):
            return ExprTraveler.constant_travel(node)

    @staticmethod
    def name_travel(node: ast.Name, elem_manager: CodeElementManager):
        return NameExpr.parse(node.ctx, node.id, elem_manager)

    @staticmethod
    def constant_travel(node: ast.Constant):
        return ConstantExpr.parse(node)

    @staticmethod
    def call_travel(node: ast.Call, elem_manager: CodeElementManager):
        func_name = ExprTraveler._get_func_name(node.func, elem_manager)
        args = ExprTraveler._get_args(node.args, elem_manager)
        keyword_dict = ExprTraveler._keywords_to_dict(node.keywords, elem_manager)

        return CallExpr.parse(func_name, args, keyword_dict)

    @staticmethod
    def _get_func_name(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.Name):
            return ExprTraveler.name_travel(node, elem_manager)

        elif isinstance(node, ast.Attribute):
            raise NotImplementedError(f"[call_travel] {type(node)}정의되지 않았습니다.")

        else:
            raise TypeError(f"[call_travel] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _get_args(args: list[ast], elem_manager: CodeElementManager):
        expressions = []

        for arg in args:
            if isinstance(arg, ast.BinOp):
                travel_result = ExprTraveler.binop_travel(arg, elem_manager)
                expressions.append(travel_result)

            elif isinstance(arg, ast.Name):
                travel_result = ExprTraveler.name_travel(arg, elem_manager)
                expressions.append(travel_result)

            elif isinstance(arg, ast.Constant):
                travel_result = ExprTraveler.constant_travel(arg)
                expressions.append(travel_result)

            else:
                raise TypeError(f"[call_travel] {type(arg)}는 잘못된 타입입니다.")

        return expressions

    @staticmethod
    def _keywords_to_dict(keywords: list, elem_manager: CodeElementManager):
        keyword_dict = {}

        for keyword in keywords:
            if isinstance(keyword.value, ast.BinOp):
                binop_obj = ExprTraveler.binop_travel(keyword.value, elem_manager)
                value = binop_obj.value

            elif isinstance(keyword.value, ast.Name):
                name_obj = ExprTraveler.name_travel(keyword.value, elem_manager)
                value = name_obj.value

            elif isinstance(keyword.value, ast.Constant):
                constant_obj = ExprTraveler.constant_travel(keyword.value)
                value = constant_obj.value

            elif isinstance(keyword.value, ast.Call):
                call_obj = ExprTraveler.call_travel(keyword.value, elem_manager)
                value = call_obj.value

            else:
                raise TypeError(f"[binop_travel] {type(keyword.value)}는 잘못된 타입입니다.")

            keyword_dict[keyword.arg] = value

        return keyword_dict
