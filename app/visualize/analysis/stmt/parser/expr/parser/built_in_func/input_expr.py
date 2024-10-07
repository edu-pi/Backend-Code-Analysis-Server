from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, InputObj
from app.visualize.container.element_container import ElementContainer


class InputExpr:

    @staticmethod
    def parse(args: list[ExprObj], elem_container: ElementContainer):
        if len(args) > 1:
            raise ValueError(
                f"[InputExpr] input() 함수는 1개 이하의 인자만 받을 수 있습니다. ({len(args)}개의 인자가 입력됨)"
            )
        value = InputExpr._get_value(elem_container)
        expressions = InputExpr._create_expressions(args, value)

        return InputObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(elem_container: ElementContainer):
        return elem_container.get_input()

    @staticmethod
    def _create_expressions(args: list[ExprObj], value):
        expressions = []
        if args:
            expressions.append('input("' + args[0].value + '")')
        else:
            expressions.append("input()")

        expressions.append(value)
        return tuple(expressions)
