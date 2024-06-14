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

    def parse(self):
        if isinstance(self.ctx, ast.Store):
            return self.__parse_store()
        elif isinstance(self.ctx, ast.Load):
            return self.__parse_load()
        else:
            raise NotImplementedError(f"Unsupported node type: {type(self.ctx)}")

    # ctx가 Store일 때 target_names를 만들어주는 함수
    def __parse_store(self):
        target_names = []

        for elt in self.elts:
            if isinstance(elt, ast.Name):
                target_names.append(elt.id)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        return TupleTargetNames(tuple(target_names))

    # ctx가 Load일 때 표현식을 만들어서 튜플로 만들어 주는 함수
    def __parse_load(self):
        expressions = []
        for elt in self.elts:
            if isinstance(elt, ast.Name):
                name = NameParser(elt, self.elem_manager).parse()
                expressions.append(name.expressions)

            elif isinstance(elt, ast.Constant):
                constant = ConstantParser(elt).parse()
                expressions.append(constant.expressions)

            elif isinstance(elt, ast.BinOp):
                binop = BinopParser(elt, self.elem_manager).parse()
                expressions.append(binop.expressions)

            else:
                raise NotImplementedError(f"Unsupported node type: {type(elt)}")

        return TupleExpressions(self.__make_tuple(expressions))

    # 변수들의 표션식 리스트를 받아와서 튜플로 만들어주는 함수
    # [["10"], ["a+13", "5+13", "28"], ["b", "4"]] -> [("10", "a+13", "b"), ("10", "5+13", "4"), ("10", "28", "4")]
    def __make_tuple(self, expressions):
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
class TupleExpressions:
    expressions: list


@dataclass
class TupleTargetNames:
    target_names: list
