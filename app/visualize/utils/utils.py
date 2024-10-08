# util 함수들을 모아놓은 파일


# 변수들의 표현식 리스트를 받아와서 배열의 행과 열을 바꿔주고 마지막 값으로 채워주는 함수
# [["10"], ["a+13", "5+13", "28"], ["b", "4"]] -> [["10", "a+13", "b"], ["10", "5+13", "4"], ["10", "28", "4"]]
def transpose_with_last_fill(expressions):

    try:
        max_length = max(len(sublist) for sublist in expressions)
    except ValueError:
        return []

    transposed_values = []
    for i in range(max_length):
        current_list = tuple(
            sublist[i] if isinstance(sublist, tuple) and i < len(sublist) else sublist[-1] for sublist in expressions
        )
        transposed_values.append(current_list)

    return transposed_values


def list_to_str(list_: list):
    return " ".join(list_)


def is_array(target):
    if isinstance(target, (list, tuple)):
        return True

    if target in ("list", "tuple"):
        return True

    return False


def is_same_len(array1, array2):
    return len(array1) == len(array2)


def getStringType(target):
    if not isinstance(target, str):
        if isinstance(target, tuple):
            return "tuple"
        elif isinstance(target, list):
            return "list"
        elif isinstance(target, dict):
            return "dict"
        else:
            return "variable"

    try:
        evaluated_value = eval(target)
    except (SyntaxError, NameError):
        return "variable"

    if isinstance(evaluated_value, list):
        return "list"
    elif isinstance(evaluated_value, tuple):
        return "tuple"
    elif isinstance(evaluated_value, dict):
        return "dict"
    else:
        return "variable"
