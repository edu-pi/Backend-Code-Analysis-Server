import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.expr.parser.attribute_expr import AttributeExpr
from app.visualize.analysis.stmt.parser.expr.parser.binop_expr import BinopExpr
from app.visualize.analysis.stmt.parser.expr.parser.call_expr import CallExpr
from app.visualize.analysis.stmt.parser.expr.parser.compare_expr import CompareExpr
from app.visualize.analysis.stmt.parser.expr.parser.constant_expr import ConstantExpr
from app.visualize.analysis.stmt.parser.expr.parser.dict_expr import DictExpr
from app.visualize.analysis.stmt.parser.expr.parser.formatted_value_expr import FormattedValueExpr
from app.visualize.analysis.stmt.parser.expr.parser.joined_str_expr import JoinedStrExpr
from app.visualize.analysis.stmt.parser.expr.parser.list_expr import ListExpr
from app.visualize.analysis.stmt.parser.expr.parser.name_expr import NameExpr
from app.visualize.analysis.stmt.parser.expr.parser.slice_expr import SliceExpr
from app.visualize.analysis.stmt.parser.expr.parser.subscript_expr import SubscriptExpr
from app.visualize.analysis.stmt.parser.expr.parser.tuple_expr import TupleExpr
from app.visualize.analysis.stmt.parser.expr.parser.unary_op_expr import UnaryOpExpr
from app.visualize.container.element_container import ElementContainer


class ExprTraveler:

    @staticmethod
    def travel(node: ast, elem_container: ElementContainer) -> ExprObj:
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

        elif isinstance(node, ast.Tuple):
            return ExprTraveler._tuple_travel(node, elem_container)

        elif isinstance(node, ast.Dict):
            return ExprTraveler._dict_travel(node, elem_container)

        elif isinstance(node, ast.Compare):
            compare_obj = ExprTraveler._compare_travel(node, elem_container)
            return compare_obj

        elif isinstance(node, ast.Subscript):
            subscript_obj = ExprTraveler._subscript_travel(node, elem_container)
            return subscript_obj

        elif isinstance(node, ast.Slice):
            slice_obj = ExprTraveler._slice_travel(node, elem_container)
            return slice_obj

        elif isinstance(node, ast.Attribute):
            attribute_obj = ExprTraveler._attribute_travel(node, elem_container)
            return attribute_obj

        elif isinstance(node, ast.UnaryOp):
            unary_op_obj = ExprTraveler._unary_op_travel(node, elem_container)
            return unary_op_obj

        elif isinstance(node, ast.FormattedValue):
            formatted_value_obj = ExprTraveler._formatted_value_travel(node, elem_container)
            return formatted_value_obj

        elif isinstance(node, ast.JoinedStr):
            joined_str_obj = ExprTraveler._joined_str_travel(node, elem_container)
            return joined_str_obj

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

        elif isinstance(node, ast.Subscript):
            return ExprTraveler._subscript_travel(node, elem_container)

        else:
            raise TypeError(f"[ExprTraveler - binop parsing 중  {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _name_travel(node: ast.Name, elem_container: ElementContainer):
        return NameExpr.parse(node, elem_container)

    @staticmethod
    def _constant_travel(node: ast.Constant):
        return ConstantExpr.parse(node)

    @staticmethod
    def _call_travel(node: ast.Call, elem_container: ElementContainer):
        func_name = ExprTraveler._get_func_name(node.func, elem_container)
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
    def _tuple_travel(node: ast.Tuple, elem_container: ElementContainer):
        elts = [ExprTraveler.travel(elt, elem_container) for elt in node.elts]
        return TupleExpr.parse(elts)

    @staticmethod
    def _dict_travel(node: ast.Dict, elem_container: ElementContainer):
        keys = [ExprTraveler.travel(key, elem_container) for key in node.keys]
        values = [ExprTraveler.travel(value, elem_container) for value in node.values]

        return DictExpr.parse(keys, values)

    @staticmethod
    def _compare_travel(node: ast, elem_container: ElementContainer):
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
    def _get_func_name(node: ast, elem_container: ElementContainer):
        if isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Attribute):
            return ExprTraveler._attribute_travel(node, elem_container)

        else:
            raise TypeError(f"[ExprTraveler] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _subscript_travel(node: ast.Subscript, elem_container: ElementContainer):
        target_obj = ExprTraveler.travel(node.value, elem_container)
        slice_obj = ExprTraveler.travel(node.slice, elem_container)

        subscript_obj = SubscriptExpr.parse(target_obj, slice_obj, node.ctx)
        return subscript_obj

    @staticmethod
    def _slice_travel(node: ast.Slice, elem_container: ElementContainer):
        lower = ExprTraveler.travel(node.lower, elem_container) if node.lower else None
        upper = ExprTraveler.travel(node.upper, elem_container) if node.upper else None
        step = ExprTraveler.travel(node.step, elem_container) if node.step else None

        return SliceExpr.parse(lower, upper, step)

    @staticmethod
    def _attribute_travel(node: ast.Attribute, elem_container: ElementContainer):
        target_obj = ExprTraveler.travel(node.value, elem_container)
        attr_name = node.attr
        return AttributeExpr.parse(target_obj, attr_name)

    @staticmethod
    def _unary_op_travel(node: ast.UnaryOp, elem_container):
        operand_obj = ExprTraveler.travel(node.operand, elem_container)
        return UnaryOpExpr.parse(node.op, operand_obj)

    def _formatted_value_travel(node: ast.FormattedValue, elem_container: ElementContainer):
        value = ExprTraveler.travel(node.value, elem_container)
        joined_str_obj = None
        if node.format_spec:
            joined_str_obj = ExprTraveler.travel(node.format_spec, elem_container)

        return FormattedValueExpr.parse(value, node.conversion, joined_str_obj)

    @staticmethod
    def _joined_str_travel(node: ast.JoinedStr, elem_container: ElementContainer):
        value_objs = [ExprTraveler.travel(value, elem_container) for value in node.values]

        return JoinedStrExpr.parse(value_objs)
