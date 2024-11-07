from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.models.assign_viz import AssignViz
from app.visualize.generator.models.variable_vlz import Variable, SubscriptIdx
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils import utils


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        expr_stmt_obj = assign_obj.expr_stmt_obj
        var_type = expr_stmt_obj.expr_type.value
        call_stack_name = assign_obj.call_stack_name

        return AssignConverter._convert_to_assign_viz(
            expr_stmt_obj, viz_manager, assign_obj.targets, var_type, call_stack_name
        )

    @staticmethod
    def convert_user_func(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        user_func_stmt_obj = assign_obj.expr_stmt_obj
        var_type = utils.getStringType(user_func_stmt_obj.expr[-1])
        call_stack_name = assign_obj.call_stack_name

        return AssignViz(
            variables=[
                Variable(
                    id=user_func_stmt_obj.id,
                    expr=user_func_stmt_obj.expr[-1],
                    name=assign_obj.targets[0],
                    code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
                    type=var_type,
                )
            ],
            callStackName=call_stack_name,
        )

    @staticmethod
    def _convert_to_assign_viz(expr_stmt_obj, viz_manager, targets, var_type: str, call_stack_name: str):
        variable_list = []

        for target in targets:
            AssignConverter._create_variable_list(expr_stmt_obj, viz_manager, target, var_type, variable_list)

        return AssignViz(variables=variable_list, callStackName=call_stack_name)

    @staticmethod
    def _create_variable_list(expr_stmt_obj, viz_manager, target, var_type: str, variable_list):

        # target이 list나 tuple일 경우
        if utils.is_array(target):
            #  value가 list나 tuple이 아닌 경우 예외
            if not utils.is_array(var_type):
                raise ValueError("target과 value의 길이가 다릅니다.")

            # target과 value의 길이가 다른 경우 예외
            if not utils.is_same_len(target, expr_stmt_obj.value):
                raise ValueError("target과 value의 길이가 다릅니다.")

            variable_list.extend(
                [
                    Variable(
                        id=expr_stmt_obj.id,
                        expr=str(expr_stmt_obj.value[idx]),
                        name=target[idx],
                        code=viz_manager.get_code_by_idx(expr_stmt_obj.id),
                        type="variable",
                    )
                    for idx in range(len(target))
                ]
            )

        elif utils.is_subscript(target):
            target, idx = utils.extract_subscript(target)
            variable_list.append(
                Variable(
                    id=expr_stmt_obj.id,
                    expr=expr_stmt_obj.expressions[-1] if expr_stmt_obj.expressions else None,
                    name=target,
                    idx=idx,
                    code=viz_manager.get_code_by_idx(expr_stmt_obj.id),
                    type=var_type,
                )
            )

        # 이외의 모든 경우
        else:
            variable_list.append(
                Variable(
                    id=expr_stmt_obj.id,
                    expr=expr_stmt_obj.expressions[-1] if expr_stmt_obj.expressions else None,
                    name=target,
                    idx=(
                        SubscriptIdx(start=0, end=len(expr_stmt_obj.value) - 1)
                        if var_type in ("list", "tuple")
                        else SubscriptIdx(start=0, end=0)
                    ),
                    code=viz_manager.get_code_by_idx(expr_stmt_obj.id),
                    type=var_type,
                )
            )
