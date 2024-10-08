from app.visualize.analysis.stmt.parser.expr.models.expr_obj import AttributeObj, ExprObj, InsertObj


class InsertExpr:

    @staticmethod
    def parse(attr_obj: AttributeObj, args: list[ExprObj]):
        if len(args) != 2:
            raise ValueError(
                f"[InsertExpr] insert() 함수는 2개의 인자만 받을 수 있습니다. ({len(args)}개의 인자가 입력됨)"
            )

        InsertExpr._insert_value(attr_obj, args)
        value = InsertExpr._get_value(attr_obj)
        expressions = InsertExpr._create_expressions(args)

        return InsertObj(value=value, expressions=expressions)

    @staticmethod
    def _insert_value(attr_obj: AttributeObj, args: list[ExprObj]):
        insert_method = attr_obj.value

        insert_method(args[0].value, args[1].value)

    @staticmethod
    def _get_value(attr_obj: AttributeObj):
        return attr_obj.expressions[0]

    @staticmethod
    def _create_expressions(args: list[ExprObj]):
        return (args[0].expressions[-1] + " " + args[1].expressions[-1],)
