import re


def replace_word(expression, original_word, new_word):
    pattern = rf"\b{original_word}\b"
    replaced_expression = re.sub(pattern, str(new_word), expression)
    return replaced_expression


# 변수들의 표현식 리스트를 받아와서 배열의 행과 열을 바꿔주고 마지막 값으로 채워주는 함수
# [["10"], ["a+13", "5+13", "28"], ["b", "4"]] -> [["10", "a+13", "b"], ["10", "5+13", "4"], ["10", "28", "4"]]
def transpose_with_last_fill(expressions):
    max_length = max(len(sublist) for sublist in expressions)

    transposed_values = []
    for i in range(max_length):
        current_list = tuple(
            sublist[i] if isinstance(sublist, tuple) and i < len(sublist) else sublist[-1] for sublist in expressions
        )
        transposed_values.append(current_list)

    return transposed_values
