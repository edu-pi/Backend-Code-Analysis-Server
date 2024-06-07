import ast
import re

from app.analysis.element_manager import CodeElementManager
from app.analysis.models import *

g_elem_manager = CodeElementManager()
print("CodeElementManager 생성")


# ast.assign 을 받아 값을 할당하고 step에 추가
def assign_parse(node):
    for target in node.targets:
        depth = g_elem_manager.depth

        # BinOp인 경우
        if isinstance(node.value, ast.BinOp):
            parsed_expressions = binOp_parse(node.value)
            for parsed_expression in parsed_expressions:
                g_elem_manager.add_step(
                    Variable(depth=depth, target=target.id, expr=parsed_expression)
                )
            g_elem_manager.add_variable_value(name=target.id, value=parsed_expressions[-1])

        # 상수인 경우
        elif isinstance(node.value, ast.Constant):
            value = constant_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.add_step(
                Variable(depth=depth, target=target.id, expr=g_elem_manager.get_variable_value(name=target.id))
            )

        # 변수인 경우
        elif isinstance(node.value, ast.Name):
            g_elem_manager.add_step(
                Variable(depth=depth, target=target.id, expr=node.id)
            )
            value = name_parse(node.value)
            g_elem_manager.add_variable_value(name=target.id, value=value)
            g_elem_manager.add_step(
                Variable(depth=depth, target=target.id, expr=value)
            )


def replace_variable(expression, variable, key):
    pattern = rf'\b{variable}\b'
    replaced_expression = re.sub(pattern, str(key), expression)
    return replaced_expression


def binOp_parse(node):
    value = __calculate_binOp_result(node, ast.unparse(node))
    return __create_intermediate_expression(ast.unparse(node), value)


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
    try:
        return g_elem_manager.get_variable_value(name=node.id)
    except NameError as e:
        print("#error:", e)


def constant_parse(node):
    return node.value


def for_parse(node):
    # 타겟 처리
    target_name = node.target.id
    for_id = g_elem_manager.get_call_id(node)

    # Condition 객체 생성
    pre_condition = None
    origin_condition = create_condition(target_name, node.iter)

    # for문 수행
    for i in range(origin_condition.start, origin_condition.end, origin_condition.step):
        # target 업데이트
        g_elem_manager.add_variable_value(name=target_name, value=i)
        cur_condition = create_condition(target_name, node.iter)

        # 변경된 속성 이름 찾기
        highlight = cur_condition.changed_attr(pre_condition)
        pre_condition = cur_condition

        # for step 추가
        g_elem_manager.add_step(
            For(id=for_id, depth=g_elem_manager.get_depth(), condition=cur_condition, highlight=highlight)
        )
        g_elem_manager.increase_depth()

        for child_node in node.body:
            if isinstance(child_node, ast.Expr):
                parsed_objs = expr_parse(child_node)
                if parsed_objs is None:
                    continue

                # for parsed_obj in parsed_objs:
                #     g_elem_manager.add_step(parsed_obj)

            elif isinstance(child_node, ast.For):
                for_parse(child_node)
        g_elem_manager.decrease_depth()


def expr_parse(node: ast.Expr):
    if isinstance(node.value, ast.Call):
        return call_parse(node.value)


def call_parse(node: ast.Call):
    func_name = node.func.id

    if func_name == 'print':
        return print_parse(node)


def print_parse(node: ast.Call):
    print_objects = []

    for cur_node in node.args:
        if isinstance(cur_node, ast.BinOp):
            # 연산 과정 리스트 생성
            parsed_expressions = binOp_parse(cur_node)
            # 중간 연산 과정이 포함된 노드 생성
            for parsed_expression in parsed_expressions:
                print_obj = Print(id=g_elem_manager.get_call_id(node), depth=g_elem_manager.get_depth(),
                                  expr=parsed_expression)
                print_objects.append(print_obj)  # 리스트에 추가

    return print_objects


def create_condition(target_name, node: ast.Call):
    # Condition - start, end, step
    start = 0
    end = None
    step = 1

    # args의 개수에 따라 start, end, step에 값을 할당
    identifier_list = [identifier_parse(arg) for arg in node.args]

    if len(identifier_list) == 1:
        end = identifier_list[0]
    elif len(identifier_list) == 2:
        start, end = identifier_list
    elif len(identifier_list) == 3:
        start, end, step = identifier_list

    try:
        cur = g_elem_manager.get_variable_value(target_name)
    except NameError:
        # 기존에 선언되지 않는 변수라면 0으로 초기화
        cur = g_elem_manager.add_variable_value(target_name, 0)
    return Condition(target=target_name, start=start, end=end, step=step, cur=cur)


def identifier_parse(arg):
    if isinstance(arg, ast.Name):  # 변수 이름인 경우
        return name_parse(arg)
    elif isinstance(arg, ast.Constant):  # 상수인 경우
        return constant_parse(arg)
    else:
        raise TypeError(f"Unsupported node type: {type(arg)}")
