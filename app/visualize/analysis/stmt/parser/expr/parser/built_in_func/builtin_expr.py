import builtins

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, BuiltinObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.utils import utils


class BuiltinExpr:

    @staticmethod
    def parse(func_name, args: list[ExprObj]):
        value = BuiltinExpr._get_value(func_name, args)
        expressions = BuiltinExpr._create_expressions(func_name, args, value)

        var_type = utils.getStringType(value)
        if var_type == "variable":
            return BuiltinObj(value=value, expressions=expressions, type=ExprType(var_type))

        elif var_type in {"tuple", "dict", "list"}:
            return BuiltinObj(value=value, expressions=(expressions[-1],), type=ExprType(var_type))

        else:
            raise TypeError(f"[BuiltinExpr]:{var_type}는 지원하지 않습니다.")

    @staticmethod
    def is_builtin_func(func_name):
        if func_name in dir(builtins) and callable(getattr(builtins, func_name)):
            return True
        else:
            return False

    @staticmethod
    def _get_value(func_name, args):
        func = getattr(builtins, func_name)
        values = [arg.value for arg in args]

        try:
            return func(*values)

        except Exception as e:
            NotImplementedError(f"[BuiltinExpr]:{func_name}은 지원하지 않습니다.")

    @staticmethod
    def _create_expressions(func_name: str, args: list[ExprObj], value):
        expressions = []
        if args:
            expressions.append(f"{func_name}({', '.join(repr(arg.value) for arg in args)})")
        else:
            expressions.append("")

        expressions.append(str(value))
        return tuple(expressions)
