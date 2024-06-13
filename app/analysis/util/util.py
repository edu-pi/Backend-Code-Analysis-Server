import re


def replace_word(expression, original_word, new_word):
    pattern = rf'\b{original_word}\b'
    replaced_expression = re.sub(pattern, str(new_word), expression)
    return replaced_expression
