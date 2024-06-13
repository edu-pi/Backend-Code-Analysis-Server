import re


def replace_variable(expression, variable, key):
    pattern = rf'\b{variable}\b'
    replaced_expression = re.sub(pattern, str(key), expression)
    return replaced_expression
