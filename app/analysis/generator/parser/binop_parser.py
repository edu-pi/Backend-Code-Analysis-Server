import ast
import re
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.util.util import replace_word


class BinopParser:

    def __init__(self, node: ast.BinOp, elem_manager: CodeElementManager):
        self.node = node
        self.elem_manager = elem_manager

    def parse(self):
        value = self.__calculate_value(self.node)
        expressions = self.__create_expressions(ast.unparse(self.node), value)
        return Binop(value, expressions)

    # 연산식을 따라가면서 계산해 결과를 반환
    def __calculate_value(self, node):
        if isinstance(node, ast.BinOp):
            left = self.__calculate_value(node.left)
            right = self.__calculate_value(node.right)
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
            name = NameParser(node, self.elem_manager).parse()
            return name.value
        elif isinstance(node, ast.Constant):
            constant = ConstantParser(node).parse()
            return constant.value
        else:
            raise NotImplementedError(f"Unsupported node type: {type(node)}")

    def __create_expressions(self, expr, result):
        # 초기 계산식 저장
        expr_results = [expr]
        pattern = r'\b[a-zA-Z_]\w*\b'
        var_names = set(re.findall(pattern, expr))

        # 변수들을 값으로 대체
        for var in var_names:
            value = self.elem_manager.get_variable_value(var)
            expr = replace_word(expression=expr, original_word=var, new_word=value)

        if len(var_names) != 0:
            expr_results.append(expr)

        # 마지막 계산 결과 저장
        expr_results.append(result)
        return expr_results


@dataclass
class Binop:
    value: int
    expressions: list
