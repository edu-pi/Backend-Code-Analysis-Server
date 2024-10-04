from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, AttributeObj, PopObj


class PopExpr:

    @staticmethod
    def parse(attr_obj: AttributeObj, args: list[ExprObj]):
        if len(args) != 0:
            raise ValueError(f"[PopExpr] pop() 함수는 1개의 인자만 받을 수 있습니다. ({len(args)}개의 인자가 입력됨)")

        return_value = PopExpr._pop_value(attr_obj)

        value = PopExpr._get_value(attr_obj)
        expressions = PopExpr._create_expressions(return_value)

        return PopObj(value=value, expressions=expressions)

    @staticmethod
    def _pop_value(attr_obj: AttributeObj):
        remove_method = attr_obj.value

        return remove_method()

    @staticmethod
    def _get_value(attr_obj: AttributeObj):
        return attr_obj.expressions[0]

    @staticmethod
    def _create_expressions(return_value):
        return (str(return_value),)
