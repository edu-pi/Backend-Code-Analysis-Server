from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.models.assign_viz import AssignViz
from app.visualize.generator.models.variable_vlz import Variable
from app.visualize.utils import utils


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj):
        expr_stmt_obj = assign_obj.expr_stmt_obj
        var_type = utils.get_var_type(expr_stmt_obj.value, expr_stmt_obj.expr_type)

        return AssignConverter._convert_to_assign_viz(expr_stmt_obj, assign_obj.targets, var_type)

    # Todo 함수 분리
    @staticmethod
    def _convert_to_assign_viz(expr_stmt_obj, targets, var_type):
        variable_list = []

        for target in targets:
            # target과 var_type이 모두 list나 tuple일 경우
            if utils.is_array(target):
                if not utils.is_array(var_type):
                    variable_list.extend(
                        [
                            Variable(
                                id=expr_stmt_obj.id,
                                expr=expr_stmt_obj.expressions[-1],
                                name=t,
                                type=var_type,
                            )
                            for t in target
                        ]
                    )

                if utils.is_array(var_type) and utils.is_same_len(target, expr_stmt_obj.value):
                    variable_list.extend(
                        [
                            Variable(
                                id=expr_stmt_obj.id,
                                expr=str(expr_stmt_obj.value[idx]),
                                name=target[idx],
                                type="variable",
                            )
                            for idx in range(len(target))
                        ]
                    )
            else:
                variable_list.append(
                    Variable(
                        id=expr_stmt_obj.id,
                        expr=expr_stmt_obj.expressions[-1],
                        name=target,
                        type=var_type,
                    )
                )

        return AssignViz(variables=variable_list)

    @staticmethod
    def _get_var_type(var_type: str):
        if var_type in ("name", "constant", "binop"):
            var_type = "variable"

        return var_type
