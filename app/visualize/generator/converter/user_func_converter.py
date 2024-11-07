from app.visualize.analysis.stmt.models.user_func_stmt_obj import UserFuncStmtObj
from app.visualize.generator.models.user_func_viz import CallUserFuncViz, CreateCallStackViz, Argument, EndUserFuncViz
from app.visualize.generator.models.variable_vlz import SubscriptIdx
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils.utils import getStringType


class UserFuncConverter:

    @staticmethod
    def convert_to_call_user_func(user_func_stmt_obj: UserFuncStmtObj, viz_manager: VisualizationManager):

        return CallUserFuncViz(
            id=user_func_stmt_obj.id,
            assignName=user_func_stmt_obj.return_argument_name,
            depth=viz_manager.get_depth(),
            signature=user_func_stmt_obj.func_signature[0],
            code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
        )

    @staticmethod
    def convert_to_create_call_stack(user_func_stmt_obj: UserFuncStmtObj, viz_manager: VisualizationManager):
        arguments = [
            Argument(
                id=user_func_stmt_obj.id,
                expr=str(arg_value),
                name=arg_name,
                type=getStringType(arg_value),
                code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
                idx=(
                    SubscriptIdx(start=0, end=len(arg_value) - 1)
                    if getStringType(arg_value) == "list"
                    else SubscriptIdx(start=0, end=0)
                ),
            )
            for arg_name, arg_value in user_func_stmt_obj.args.items()
        ]

        return CreateCallStackViz(
            id=user_func_stmt_obj.id,
            args=arguments,
            callStackName=user_func_stmt_obj.func_name,
            code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
        )

    @staticmethod
    def convert_to_end_user_func(user_func_stmt_obj: UserFuncStmtObj, targets, viz_manager: VisualizationManager):

        return EndUserFuncViz(
            id=user_func_stmt_obj.id,
            depth=viz_manager.get_depth(),
            returnExpr=user_func_stmt_obj.expr[-1],
            returnArgName="" if len(targets) == 0 else targets[0],
            code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
            delFuncName=user_func_stmt_obj.func_name,
        )
