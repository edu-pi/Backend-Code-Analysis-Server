import ast
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser


class TupleParser:

    def __init__(self, node: ast.Tuple, elem_manager: CodeElementManager):
        self.ctx = node.ctx
        self.elts = node.elts
        self.elem_manager = elem_manager

    # ast.ctx가 Store인 경우엔 target_names 사용
    # ast.ctx가 Load인 경우엔 expressions 사용
    def parse(self):
        if isinstance(self.ctx, ast.Store):
            target_names = self.__get_target_names()
            tuple_result = {}

        elif isinstance(self.ctx, ast.Load):
            target_names = []
            tuple_result = self.__calculate_node()

        else:
            raise NotImplementedError(f"Unsupported node type: {type(self.ctx)}")

        return Tuple(
            target_names=tuple(target_names),
            value=tuple_result.get("value", None),
            expressions=tuple_result.get("expressions", None)
        )

    # ctx가 Store일 때 target_names를 만들어주는 함수
    def __get_target_names(self):
        target_names = []

        for elt in self.elts:
            if isinstance(elt, ast.Name):
                name = NameParser(elt, self.elem_manager).parse()
                target_names.append(name.id)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        return target_names

    # ctx가 Load일 때 tuple을 계산해 value와 expression을 계산하는 함수
    def __calculate_node(self):
        tuple_value = []
        tuple_expressions = []
        for elt in self.elts:
            if isinstance(elt, ast.Name):
                name_obj = NameParser(elt, self.elem_manager).parse()
                tuple_value.append(name_obj.value)
                tuple_expressions.append(name_obj.expressions)

            elif isinstance(elt, ast.Constant):
                constant_obj = ConstantParser(elt).parse()
                tuple_value.append(constant_obj.value)
                tuple_expressions.append(constant_obj.expressions)

            elif isinstance(elt, ast.BinOp):
                binop_obj = BinopParser(elt, self.elem_manager).parse()
                tuple_value.append(binop_obj.value)
                tuple_expressions.append(binop_obj.expressions)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        return {"value": tuple(tuple_value), "expressions": self.__convert_expressions_to_tuple(tuple_expressions)}

    # 변수들의 표션식 리스트를 받아와서 튜플로 만들어주는 함수
    # [["10"], ["a+13", "5+13", "28"], ["b", "4"]] -> [("10", "a+13", "b"), ("10", "5+13", "4"), ("10", "28", "4")]
    def __convert_expressions_to_tuple(self, expressions):
        max_length = max(len(sublist) for sublist in expressions)

        tuple_value = []
        for i in range(max_length):
            current_tuple = tuple(
                sublist[i] if isinstance(sublist, list) and i < len(sublist) else sublist[-1]
                for sublist in expressions
            )
            tuple_value.append(current_tuple)

        return tuple_value


@dataclass
class Tuple:
    target_names: tuple
    value: tuple
    expressions: list
