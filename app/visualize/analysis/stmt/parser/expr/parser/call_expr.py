from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, RangeObj, PrintObj, AttributeObj
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.append_expr import AppendExpr
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.print_expr import PrintExpr
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.range_expr import RangeExpr

from app.visualize.utils import utils


class CallExpr:

    @staticmethod
    def parse(func_name: str | AttributeObj, args: list[ExprObj], keyword_arg_dict: dict):

        if isinstance(func_name, str):
            return CallExpr._built_in_call_parse(func_name, args, keyword_arg_dict)

        elif isinstance(func_name, AttributeObj):
            return CallExpr._attribute_call_parse(func_name, args, keyword_arg_dict)

    @staticmethod
    def _built_in_call_parse(func_name: str, args: list[ExprObj], keyword_arg_dict: dict):
        if func_name == "print":
            print_obj = PrintExpr.parse(args, keyword_arg_dict)
            return print_obj

        elif func_name == "range":
            range_obj = RangeExpr.parse(args)
            return range_obj

        else:
            raise NotImplementedError(f"[CallParser]: {func_name} 은 아직 지원하지 않습니다.")

    @staticmethod
    def _attribute_call_parse(attr_obj: AttributeObj, args: list[ExprObj], keyword_arg_dict: dict):

        if attr_obj.type == "append":
            append_obj = AppendExpr.parse(attr_obj, args, keyword_arg_dict)
            return append_obj

        else:
            raise NotImplementedError(f"[CallParser]: {attr_obj.type} 은 아직 지원하지 않습니다.")
