import ast
import re
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.util.util import replace_word


class BinopParser:

    def __init__(self, node: ast.BinOp, elem_manager: CodeElementManager):
        self.__elem_manager = elem_manager
        self.__left = node.left
        self.__op = node.op
        self.__right = node.right
        self.__initial_expression = ast.unparse(node)

    @staticmethod
    def parse(node: ast.BinOp, elem_manager: CodeElementManager):

        binop_parser = BinopParser(node, elem_manager)

        # 왼쪽, 오른쪽 노드를 계산
        left = binop_parser.__calculate_node(node.left)
        right = binop_parser.__calculate_node(node.right)

        # 계산 결과를 연산자에 따라 계산
        result = binop_parser.__calculate_value(left, right)
        expressions = binop_parser.__create_expressions(result)

        return Binop(result, expressions)

    # 연산식을 따라가면서 계산해 결과를 반환
    def __calculate_node(self, node: ast):
        if isinstance(node, ast.BinOp):
            binop = BinopParser.parse(node, self.__elem_manager)
            return binop.value

        elif isinstance(node, ast.Name):
            name = NameParser.parse(node, self.__elem_manager)
            return name.value

        elif isinstance(node, ast.Constant):
            constant = ConstantParser.parse(node)
            return constant.value

        else:
            raise NotImplementedError(f"Unsupported node type: {type(node)}")

    # 왼쪽 오른쪽 값으로 연산식 계산
    def __calculate_value(self, left: int, right: int):
        if isinstance(self.__op, ast.Add):
            return left + right

        elif isinstance(self.__op, ast.Sub):
            return left - right

        elif isinstance(self.__op, ast.Mult):
            return left * right

        elif isinstance(self.__op, ast.Div):  # '/'
            return left / right  # 실수로 계산

        elif isinstance(self.__op, ast.FloorDiv):  # '//'
            return left // right  # 정수로 계산

        else:
            raise NotImplementedError(f"Unsupported operator: {type(self.__op)}")

    def __create_expressions(self, result: int):
        # 초기 계산식 저장
        expression = self.__initial_expression
        expressions = [expression]
        pattern = r'\b[a-zA-Z_]\w*\b'

        # 변수 이름 추출
        target_names = set(re.findall(pattern, expression))

        # 변수들을 값으로 대체
        for original_name in target_names:
            replace_value = self.__elem_manager.get_variable_value(original_name)
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
