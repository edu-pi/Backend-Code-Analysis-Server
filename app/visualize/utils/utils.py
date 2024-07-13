# util 함수들을 모아놓은 파일


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


def list_to_str(list_: list):
    return " ".join(list_)


def get_var_type(var_value, obj_type: str):
    if obj_type in ("binop", "constant"):
        return "variable"

    elif obj_type == "name" or obj_type == "subscript":
        if isinstance(var_value, list):
            return "list"

        else:
            return "variable"

    elif obj_type == "list":
        return "list"

    else:
        return obj_type
