from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, SliceObj
from app.visualize.analysis.stmt.parser.expr.models.slice_expression import SliceExpression


class SliceExpr:

    @staticmethod
    def parse(lower: ExprObj | None, upper: ExprObj | None, step: ExprObj | None):
        value = SliceExpr._get_value(lower, upper, step)
        expressions = SliceExpr._create_expressions(lower, upper, step)

        return SliceObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(lower: ExprObj | None, upper: ExprObj | None, step: ExprObj | None):
        return slice(lower.value if lower else None, upper.value if upper else None, step.value if step else None)

    @staticmethod
    def _create_expressions(
        lower: ExprObj | None, upper: ExprObj | None, step: ExprObj | None
    ) -> tuple[SliceExpression, ...]:
        slice_expressions = []

        max_length = max(
            len(lower.expressions) if lower else 0,
            len(upper.expressions) if upper else 0,
            len(step.expressions) if step else 0,
        )

        for i in range(max_length):
            slice_expressions.append(
                SliceExpression(
                    lower=(
                        lower.expressions[-1]
                        if lower and i >= len(lower.expressions)
                        else (lower.expressions[i] if lower else None)
                    ),
                    upper=(
                        upper.expressions[-1]
                        if upper and i >= len(upper.expressions)
                        else (upper.expressions[i] if upper else None)
                    ),
                    step=(
                        step.expressions[-1]
                        if step and i >= len(step.expressions)
                        else (step.expressions[i] if step else None)
                    ),
                )
            )

        if len(slice_expressions) == 0:
            slice_expressions.append(SliceExpression())

        return tuple(slice_expressions)
