import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj


class NameExpr:

    @staticmethod
    def parse(ctx: ast, identifier_name, elem_container: ElementContainer):
        if isinstance(ctx, ast.Store):
            return NameObj(value=identifier_name, expressions=(identifier_name,))

        elif isinstance(ctx, ast.Load):
            value = NameExpr._get_identifier_value(identifier_name, elem_container)
            expressions = NameExpr._create_expressions(identifier_name, value)
            return NameObj(value=value, expressions=expressions)

        elif isinstance(ctx, ast.Del):
            raise NotImplementedError(f"Unsupported node type: {type(ctx)}")

        else:
            raise TypeError(f"[call_travel] {type(ctx)}는 잘못된 타입입니다.")

    # 변수의 값을 가져오는 함수
    @staticmethod
    def _get_identifier_value(identifier_name, elem_container: ElementContainer):
        try:
            return elem_container.get_element(name=identifier_name)
        except NameError as e:
            raise NameError(f"[NameExpr]: {identifier_name}은 정의되지 않은 변수입니다.") from e

    # 변수의 변화 과정을 만들어 주는 함수
    @staticmethod
    def _create_expressions(identifier_name, value) -> tuple:
        if isinstance(value, str):
            return tuple([identifier_name, f"'{value}'"])

        return tuple([identifier_name, str(value)])
