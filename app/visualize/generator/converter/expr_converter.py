from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.models.append_viz import AttributeViz
from app.visualize.generator.models.expr_viz import ExprViz
from app.visualize.generator.models.input_viz import InputViz
from app.visualize.generator.models.print_viz import PrintViz
from app.visualize.generator.models.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils.utils import getStringType


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager):
        call_id = expr_stmt_obj.id
        depth = viz_manager.get_depth()
        var_type = expr_stmt_obj.expr_type

        if var_type is ExprType.VARIABLE:
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.LIST:
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.TUPLE:
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.DICT:
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.PRINT:
            return ExprConverter._convert_to_print_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type in (
            ExprType.APPEND,
            ExprType.EXTEND,
            ExprType.INSERT,
            ExprType.REMOVE,
        ):
            return ExprConverter._convert_to_attribute_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.POP:
            return ExprConverter._convert_to_pop_attribute_viz(expr_stmt_obj, viz_manager, call_id, depth)

        elif var_type is ExprType.INPUT:
            return ExprConverter._convert_to_input_viz(expr_stmt_obj, viz_manager, call_id, depth)

        else:
            raise TypeError(f"[ExprConverter]:{var_type}는 지원하지 않습니다.")

    @staticmethod
    def _convert_to_expr_viz(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager, call_id, depth):
        expr_vizs = [
            ExprViz(
                id=call_id,
                depth=depth,
                expr=expr_stmt_obj.expressions[idx],
                type=getStringType(expr_stmt_obj.expressions[-1]),
                code=viz_manager.get_code_by_idx(call_id),
            )
            for idx in range(len(expr_stmt_obj.expressions))
        ]

        return expr_vizs

    @staticmethod
    def _convert_to_print_viz(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager, call_id, depth):
        highlights = ExprHighlight.get_highlight_indexes_exclusive_last(expr_stmt_obj.expressions)

        print_vizs = [
            PrintViz(
                id=call_id,
                depth=depth,
                expr=expr_stmt_obj.expressions[idx],
                highlights=highlights[idx],
                console=expr_stmt_obj.value if idx == len(expr_stmt_obj.expressions) - 1 else None,
                code=viz_manager.get_code_by_idx(call_id),
            )
            for idx in range(len(expr_stmt_obj.expressions))
        ]

        return print_vizs

    @staticmethod
    def _convert_to_attribute_viz(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager, call_id, depth):
        attr_vizs = []
        expr_vizs = ExprConverter._convert_to_expr_viz(expr_stmt_obj, viz_manager, call_id, depth)
        attr_vizs.extend(expr_vizs)

        attr_vizs.append(
            AttributeViz(
                variable=Variable(
                    id=call_id,
                    expr=expr_stmt_obj.expressions[-1],
                    name=expr_stmt_obj.value,
                    code=viz_manager.get_code_by_idx(call_id),
                    type=getStringType(expr_stmt_obj.expressions[-1]),
                ),
                type=expr_stmt_obj.expr_type.value,
            )
        )

        return attr_vizs

    @staticmethod
    def _convert_to_pop_attribute_viz(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager, call_id, depth):
        attr_vizs = [
            AttributeViz(
                variable=Variable(
                    id=call_id,
                    expr=expr_stmt_obj.expressions[-1],
                    name=expr_stmt_obj.expressions[0],
                    code=viz_manager.get_code_by_idx(call_id),
                    type=getStringType(expr_stmt_obj.expressions[-1]),
                ),
                type=expr_stmt_obj.expr_type.value,
            )
        ]

        return attr_vizs
