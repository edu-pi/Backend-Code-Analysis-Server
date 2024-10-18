from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, UserFuncObj, UserFunc
from app.visualize.container.element_container import ElementContainer


class UserFuncExpr:

    @staticmethod
    def parse(func_name: str, arg_objs: list[ExprObj], elem_container: ElementContainer):
        user_func = elem_container.get_element(func_name)
        user_func_id = user_func.id
        user_func_body = user_func.body
        user_func_arg_names = user_func.args

        arguments = {}
        for arg_idx in range(len(user_func_arg_names)):
            arguments[user_func_arg_names[arg_idx]] = arg_objs[arg_idx].value

        user_func = UserFunc(id=user_func_id, name=func_name, user_func_ast=user_func_body, arguments=arguments)
        expressions = UserFuncExpr._create_expressions(func_name, user_func_arg_names)

        return UserFuncObj(value=user_func, expressions=expressions)

    @staticmethod
    def _create_expressions(func_name, user_func_arg_names: list[str]):
        args_str = ", ".join(user_func_arg_names)
        return (f"{func_name}({args_str})",)
