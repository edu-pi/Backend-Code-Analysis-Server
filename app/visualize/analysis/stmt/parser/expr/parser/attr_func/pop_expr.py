from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, AttributeObj, PopObj


class PopExpr:

    @staticmethod
    def parse(attr_obj: AttributeObj, args: list[ExprObj]):
        if len(args) != 0:
            raise ValueError(f"[PopExpr] pop() 함수는 1개의 인자만 받을 수 있습니다. ({len(args)}개의 인자가 입력됨)")

        return_value = PopExpr._pop_value(attr_obj)

        target = PopExpr._get_value(attr_obj)
        expressions = PopExpr._create_expressions(target, return_value)

        return PopObj(value=return_value, expressions=expressions)

    @staticmethod
    def _pop_value(attr_obj: AttributeObj):
        pop_method = attr_obj.value

        return pop_method()

    @staticmethod
    def _get_value(attr_obj: AttributeObj):
        return attr_obj.expressions[0]

    @staticmethod
    def _create_expressions(target, return_value):
        return (
            target,
            str(return_value),
        )
