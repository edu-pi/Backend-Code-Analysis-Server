import ast
import re

from app.analysis.element_manager import CodeElementManager
from app.analysis.models import Variable

g_elem_manager = CodeElementManager()


def assign_parse(node):
    for target in node.targets:
        depth = g_elem_manager.g_depth
        if isinstance(node.value, ast.BinOp):
            parsed_expressions = binOp_parse(node.value)
            for parsed_expression in parsed_expressions:
                g_elem_manager.addStep(
                    Variable(depth=depth, name=target.id, expr=parsed_expression)
                )
            g_elem_manager.add_variable_value(name=target.id, value=parsed_expressions[-1])
        elif isinstance(node.value, ast.Constant):
            value = constant_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.addStep(
                Variable(depth=depth, name=target.id, expr=g_elem_manager.get_variable_value(name=target.id))
            )
        elif isinstance(node.value, ast.Name):
            g_elem_manager.addStep(
                Variable(depth=depth, name=target.id, expr=node.id)
            )
            value = name_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.addStep(
                Variable(depth=depth, name=target.id, expr=value)
            )


def replace_variable(expression, variable, key):
    pattern = rf'\b{variable}\b'
    replaced_expression = re.sub(pattern, str(key), expression)
    return replaced_expression


def binOp_calculate_binOp(node, expr):
    if isinstance(node, ast.BinOp):
        left = binOp_calculate_binOp(node.left, expr)
        right = binOp_calculate_binOp(node.right, expr)
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


def binOp_calculate_expressions(expr, result):
    ret = [expr]
    pattern = r'\b[a-zA-Z]{1,2}\b'
    variables = re.findall(pattern, expr)
    for var in variables:
        value = g_elem_manager.get_variable_value(var)
        expr = replace_variable(expression=expr, variable=var, key=value)
    if len(variables) != 0:
        ret.append(expr)
    ret.append(result)
    return ret


def binOp_parse(node):
    value = binOp_calculate_binOp(node, ast.unparse(node))
    return binOp_calculate_expressions(ast.unparse(node), value)


def name_parse(node):
    return g_elem_manager.get_variable_value(node.id)


def constant_parse(node):
    return node.value


def for_parse(node):
    target_name = node.target.id
