import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj


class NameExpr:

    @staticmethod
    def parse(ctx: ast, identifier_name, elem_manager: CodeElementManager):
        if isinstance(ctx, ast.Store):
            return ExprObj(type="name", value=identifier_name, expressions=[identifier_name])

        elif isinstance(ctx, ast.Load):
            value = NameExpr._get_identifier_value(identifier_name, elem_manager)
            expressions = NameExpr._create_expressions(identifier_name, value)
            return ExprObj(type="name", value=value, expressions=expressions)

        elif isinstance(ctx, ast.Del):
            raise NotImplementedError(f"Unsupported node type: {type(ctx)}")

        else:
            raise TypeError(f"[call_travel] {type(ctx)}는 잘못된 타입입니다.")

    # 변수의 값을 가져오는 함수
    @staticmethod
    def _get_identifier_value(identifier_name, elem_manager: CodeElementManager):
        try:
            return elem_manager.get_variable_value(name=identifier_name)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    @staticmethod
    def _create_expressions(identifier_name, value):
        return [identifier_name, str(value)]
