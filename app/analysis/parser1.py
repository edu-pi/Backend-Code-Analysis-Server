import ast
import re

from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.highlight import for_highlight, expressions_highlight_indices, create_highlighted_expression
from app.analysis.models import *
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser


def for_parse(node, elem_manager):
    steps = []
    # 타겟 처리
    target_name = node.__target.id
    for_id = elem_manager.get_call_id(node)

    # Condition 객체 생성
    condition = create_condition(target_name, node.__iter, elem_manager)

    # for문 수행
    for i in range(condition.start, condition.end, condition.step):
        # target 업데이트
        elem_manager.add_variable_value(name=target_name, value=i)
        # highlight 속성 생성
        highlight = for_highlight(condition)

        # for step 추가
        steps.append(
            For(id=for_id, depth=elem_manager.get_depth(), condition=condition, highlight=highlight)
        )
        elem_manager.increase_depth()

        for child_node in node.__body:
            if isinstance(child_node, ast.Expr):
                parsed_objs = expr_parse(child_node, elem_manager)
                if parsed_objs is None:
                    continue

                for parsed_obj in parsed_objs:
                    steps.append(parsed_obj)

            elif isinstance(child_node, ast.For):
                for_parse(child_node, elem_manager)
        elem_manager.decrease_depth()

        # condition 객체에서 cur 값만 변경한 새로운 condition 생성
        condition = condition.copy_with_new_cur(i + condition.step)

    return steps


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

