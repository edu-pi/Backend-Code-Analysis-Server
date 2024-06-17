import ast
from dataclasses import dataclass
from typing import Optional

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.util import util


class TupleParser:

    def __init__(self, node: ast.Tuple, elem_manager: CodeElementManager):
        self.__ctx = node.ctx
        self.__elts = node.elts
        self.__elem_manager = elem_manager

    # ast.ctx가 Store인 경우엔 target_names 사용
    # ast.ctx가 Load인 경우엔 expressions 사용
    @staticmethod
    def parse(node: ast.Tuple, elem_manager: CodeElementManager):
        tuple_parser = TupleParser(node, elem_manager)

        if isinstance(node.ctx, ast.Store):
            target_names = tuple_parser.__get_target_names()
            return Tuple(target_names=tuple(target_names))

        elif isinstance(node.ctx, ast.Load):
            tuple_result = tuple_parser.__calculate_node()
            return Tuple(
                value=tuple_result.get("value", None),
                expressions=tuple_result.get("expressions", None)
            )

        else:
            raise NotImplementedError(f"Unsupported node type: {type(node.ctx)}")

    # ctx가 Store일 때 target_names를 만들어주는 함수
    def __get_target_names(self):
        target_names = []

        for elt in self.__elts:
            if isinstance(elt, ast.Name):
                name = NameParser.parse(elt, self.__elem_manager)
                target_names.append(name.id)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        return target_names

    # ctx가 Load일 때 tuple을 계산해 value와 expression을 계산하는 함수
    def __calculate_node(self):
        tuple_value = []
        expressions = []
        for elt in self.__elts:
            if isinstance(elt, ast.Name):
                name_obj = NameParser.parse(elt, self.__elem_manager)
                tuple_value.append(name_obj.value)
                expressions.append(name_obj.expressions)

            elif isinstance(elt, ast.Constant):
                constant_obj = ConstantParser.parse(elt)
                tuple_value.append(constant_obj.value)
                expressions.append(constant_obj.expressions)

            elif isinstance(elt, ast.BinOp):
                binop_obj = BinopParser.parse(elt, self.__elem_manager)
                tuple_value.append(binop_obj.value)
                expressions.append(binop_obj.expressions)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        transposed_expressions = util.transpose_with_last_fill(expressions)
        tuple_expressions = list(map(tuple, transposed_expressions))

        return {"value": tuple(tuple_value),
                "expressions": tuple_expressions}


@dataclass
class Tuple:
    target_names: Optional[tuple] = None
    value: Optional[tuple] = None
    expressions: Optional[list] = None
