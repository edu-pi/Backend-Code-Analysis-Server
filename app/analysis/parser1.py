import ast
import re

from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.highlight import for_highlight, expressions_highlight_indices, create_highlighted_expression
from app.analysis.models import *
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser


# ast.assign 을 받아 값을 할당하고 step에 추가
def assign_parse(node, elem_manager):
    steps = []

    # value expressions 생성
    target_names = __find_target_names(node.targets)
    parsed_expressions = __value_expressions(node.value, elem_manager)

    for target_name in target_names:
        elem_manager.add_variable_value(name=target_name, value=parsed_expressions[-1])

    # elem 저장
    var_list = __create_variables(target_names, parsed_expressions, elem_manager.depth)
    steps += var_list

    return steps


def __find_target_names(targets):
    target_names = []
    for target in targets:
        if isinstance(target, ast.Name):
            target_names.append(target.id)
        elif isinstance(target, ast.Tuple):
            target_names.append(tuple(elt.id for elt in target.elts))

    return target_names


def __value_expressions(node, elem_manager):
    parsed_expressions = []

    if isinstance(node, ast.BinOp):
        binop = BinopParser(node, elem_manager).parse()
        parsed_expressions += binop.expressions

    # 상수인 경우
    elif isinstance(node, ast.Constant):
        constant = ConstantParser(node).parse()
        parsed_expressions.append(constant.value)

    # 변수인 경우
    elif isinstance(node, ast.Name):
        name = NameParser(node, elem_manager).parse()
        parsed_expressions.append(name.expressions)

    elif isinstance(node, ast.Tuple):
        parsed_expressions += tuple_parse(node, elem_manager)

    return parsed_expressions


def __create_variables(target_names, parsed_expressions, depth):
    var_lists = []

    for parsed_expression in parsed_expressions:
        variables = []
        for target_name in target_names:
            if isinstance(target_name, tuple):
                for idx in range(len(target_name)):
                    variables.append(Variable(depth, str(parsed_expression[idx]), target_name[idx]))
            else:
                variables.append(Variable(depth, str(parsed_expression), target_name))
        var_lists.append(Variables(variables))

    return var_lists


def for_parse(node, elem_manager):
    # 타겟 처리
    target_name = node.target.id
    for_id = elem_manager.get_call_id(node)

    # Condition 객체 생성
    condition = create_condition(target_name, node.iter, elem_manager)

    # for문 수행
    for i in range(condition.start, condition.end, condition.step):
        # target 업데이트
        elem_manager.add_variable_value(name=target_name, value=i)
        # highlight 속성 생성
        highlight = for_highlight(condition)

        # for step 추가
        elem_manager.add_step(
            For(id=for_id, depth=elem_manager.get_depth(), condition=condition, highlight=highlight)
        )
        elem_manager.increase_depth()

        for child_node in node.body:
            if isinstance(child_node, ast.Expr):
                parsed_objs = expr_parse(child_node, elem_manager)
                if parsed_objs is None:
                    continue

                for parsed_obj in parsed_objs:
                    elem_manager.add_step(parsed_obj)

            elif isinstance(child_node, ast.For):
                for_parse(child_node, elem_manager)
        elem_manager.decrease_depth()

        # condition 객체에서 cur 값만 변경한 새로운 condition 생성
        condition = condition.copy_with_new_cur(i + condition.step)


def expr_parse(node: ast.Expr, elem_manager):
    if isinstance(node.value, ast.Call):
        return call_parse(node.value, elem_manager)


def call_parse(node: ast.Call, elem_manager):
    func_name = node.func.id

    if func_name == 'print':
        return print_parse(node, elem_manager)


def print_parse(node: ast.Call, elem_manager):
    print_objects = []

    for cur_node in node.args:
        if isinstance(cur_node, ast.BinOp):
            binop = BinopParser(cur_node, elem_manager).parse()
            # 연산 과정 리스트 생성
            parsed_expressions = binop.expressions
            # highlight 요소 생성
            highlights = expressions_highlight_indices(parsed_expressions)
            # 중간 연산 과정이 포함된 노드 생성
            for idx, parsed_expression in enumerate(parsed_expressions):
                # 확인용 함수
                highlight_expr = create_highlighted_expression(parsed_expression, highlights[idx])
                print_obj = Print(id=elem_manager.get_call_id(node), depth=elem_manager.get_depth(),
                                  expr=parsed_expression, highlight=highlights[idx])
                print_objects.append(print_obj)

    return print_objects


def create_condition(target_name, node: ast.Call, elem_manager):
    # Condition - start, end, step
    start = 0
    end = None
    step = 1

    # args의 개수에 따라 start, end, step에 값을 할당
    identifier_list = []
    for arg in node.args:
        if isinstance(arg, ast.Name) or isinstance(arg, ast.Constant):
            identifier_list.append(identifier_parse(arg, elem_manager))
        elif isinstance(arg, ast.BinOp):
            binop = BinopParser(arg, elem_manager).parse()
            identifier_list.append(binop.value)
        else:
            raise TypeError(f"Unsupported node type: {type(arg)}")

    if len(identifier_list) == 1:
        end = identifier_list[0]
    elif len(identifier_list) == 2:
        start, end = identifier_list
    elif len(identifier_list) == 3:
        start, end, step = identifier_list

    return Condition(target=target_name, start=start, end=end, step=step, cur=start)


def identifier_parse(node, elem_manager):
    if isinstance(node, ast.Name):  # 변수 이름인 경우
        name = NameParser(node, elem_manager).parse()
        return name.value
    elif isinstance(node, ast.Constant):  # 상수인 경우
        constant = ConstantParser(node).parse()
        return constant.value
    else:
        raise TypeError(f"Unsupported node type: {type(node)}")


def tuple_parse(node, elem_manager):
    expressions = []
    tuple_value = []
    for elt in node.elts:
        if isinstance(elt, ast.Name) or isinstance(elt, ast.Constant):
            expr = identifier_parse(elt, elem_manager)
        elif isinstance(elt, ast.BinOp):
            binop = BinopParser(elt, elem_manager).parse()
            expr = binop.expressions
        else:
            raise TypeError(f"Unsupported node type: {type(elt)}")
        expressions.append(expr)

    max_length = max(len(sublist) if isinstance(sublist, list) else 1 for sublist in expressions)

    # 최대 길이만큼 반복하여 튜플을 생성
    for i in range(max_length):
        # 현재 인덱스 i에 대한 튜플을 생성
        current_tuple = tuple(
            sublist[i]
            if isinstance(sublist, list) and i < len(sublist)
            else sublist[-1]
            if isinstance(sublist, list)
            else sublist
            for sublist in expressions
        )
        # 결과 리스트에 현재 튜플 추가
        tuple_value.append(current_tuple)

    return tuple_value
