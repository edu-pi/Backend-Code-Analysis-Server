import ast
import re

from app.analysis.element_manager import CodeElementManager
from app.analysis.models import Variable, Condition, For

g_elem_manager = CodeElementManager()


def assign_parse(node):
    for target in node.targets:
        depth = g_elem_manager.g_depth
        if isinstance(node.value, ast.BinOp):
            parsed_expressions = binOp_parse(node.value)
            for parsed_expression in parsed_expressions:
                g_elem_manager.add_step(
                    Variable(depth=depth, name=target.id, expr=parsed_expression)
                )
            g_elem_manager.add_variable_value(name=target.id, value=parsed_expressions[-1])
        elif isinstance(node.value, ast.Constant):
            value = constant_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.add_step(
                Variable(depth=depth, name=target.id, expr=g_elem_manager.get_variable_value(name=target.id))
            )
        elif isinstance(node.value, ast.Name):
            g_elem_manager.add_step(
                Variable(depth=depth, name=target.id, expr=node.id)
            )
            value = name_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.add_step(
                Variable(depth=depth, name=target.id, expr=value)
            )


def replace_variable(expression, variable, key):
    pattern = rf'\b{variable}\b'
    replaced_expression = re.sub(pattern, str(key), expression)
    return replaced_expression


def binOp_parse(node):
    result = __calculate_binOp_result(node, ast.unparse(node))
    return __create_intermediate_expression(ast.unparse(node), result)


def __calculate_binOp_result(node, expr):
    if isinstance(node, ast.BinOp):
        left = __calculate_binOp_result(node.left, expr)
        right = __calculate_binOp_result(node.right, expr)
        if isinstance(node.op, ast.Add):
            value = left + right
        elif isinstance(node.op, ast.Sub):
            value = left - right
        elif isinstance(node.op, ast.Mult):
            value = left * right
        elif isinstance(node.op, ast.Div):
            value = left / right
        else:
            raise NotImplementedError(f"Unsupported operator: {type(node.op)}")
        return value
    elif isinstance(node, ast.Name):
        return name_parse(node)
    elif isinstance(node, ast.Constant):
        return constant_parse(node)
    else:
        raise NotImplementedError(f"Unsupported node type: {type(node)}")


def __create_intermediate_expression(expr, result):
    expr_results = [expr]
    pattern = r'\b[a-zA-Z]{1,2}\b'
    variables = re.findall(pattern, expr)
    for var in variables:
        value = g_elem_manager.get_variable_value(var)
        expr = replace_variable(expression=expr, variable=var, key=value)
    if len(variables) != 0:
        expr_results.append(expr)
    expr_results.append(result)
    return expr_results


def name_parse(node):
    return g_elem_manager.get_variable_value(node.id)


def constant_parse(node):
    return node.value


def for_parse(node):
    target_name = node.target.id
    condition = call_parse(node.iter, target_name)

    g_elem_manager.g_depth = g_elem_manager.g_depth + 1
    for i in range(condition.start, condition.end, condition.step):
        for_node = For(id=id(condition), depth=g_elem_manager.g_depth, condition=condition)
        g_elem_manager.add_step(for_node)
        for expr_node in node.body:
            g_elem_manager.add_variable_value(name=target_name, value=i)
            from app.analysis.code_analyzer import parse_node
            parse_node(expr_node, target_name)

        condition = condition.copy_with_new_cur(i + condition.step)


def call_parse(node, target_name):
    start, end, step = 0, None, 1

    identifier_list = [__parse_identifier(arg) for arg in node.args]
    length = len(identifier_list)

    if length == 1:
        end = identifier_list[0]
    elif length == 2:
        start, end = identifier_list
    elif length == 3:
        start, end, step = identifier_list
    return Condition(name=target_name, start=start, end=end, step=step, cur=start)


def __parse_identifier(node):
    if isinstance(node, ast.Name):
        return name_parse(node)
    elif isinstance(node, ast.Constant):
        return constant_parse(node)
