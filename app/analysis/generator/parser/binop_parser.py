import ast
import re
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.util.util import replace_word


class BinopParser:

    @staticmethod
    def parse(node: ast.BinOp, elem_manager: CodeElementManager):
        # 왼쪽, 오른쪽 노드를 계산
        left = BinopParser.__calculate_node(node.left, elem_manager)
        right = BinopParser.__calculate_node(node.right, elem_manager)

        # 계산 결과를 연산자에 따라 계산
        result = BinopParser.__calculate_value(left, right, node.op)
        expressions = BinopParser.__create_expressions(node, result, elem_manager)

        return Binop(result, expressions)

    # 연산식을 따라가면서 계산해 결과를 반환
    @staticmethod
    def __calculate_node(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.BinOp):
            binop = BinopParser.parse(node, elem_manager)
            return binop.value

        elif isinstance(node, ast.Name):
            name = NameParser.parse(node, elem_manager)
            return name.value

        elif isinstance(node, ast.Constant):
            constant = ConstantParser.parse(node)
            return constant.value

        else:
            raise NotImplementedError(f"Unsupported node type: {type(node)}")

    # 왼쪽 오른쪽 값으로 연산식 계산
    @staticmethod
    def __calculate_value(left: int, right: int, op: ast):
        if isinstance(op, ast.Add):
            return left + right

        elif isinstance(op, ast.Sub):
            return left - right

        elif isinstance(op, ast.Mult):
            return left * right

        elif isinstance(op, ast.Div):
            return left / right

        else:
            raise NotImplementedError(f"Unsupported operator: {type(op)}")

    @staticmethod
    def __create_expressions(node: ast.BinOp, result: int, elem_manager: CodeElementManager):
        # 초기 계산식 저장
        expression = ast.unparse(node)
        expressions = [expression]
        pattern = r'\b[a-zA-Z_]\w*\b'

        # 변수 이름 추출
        target_names = set(re.findall(pattern, expression))

        # 변수들을 값으로 대체
        for original_name in target_names:
            replace_value = elem_manager.get_variable_value(original_name)
            expression = replace_word(expression=expression, original_word=original_name, new_word=replace_value)

        if len(target_names) != 0:
            expressions.append(expression)

        # 마지막 계산 결과 저장
        expressions.append(str(result))

        return expressions


@dataclass
class Binop:
    value: int
    expressions: list
