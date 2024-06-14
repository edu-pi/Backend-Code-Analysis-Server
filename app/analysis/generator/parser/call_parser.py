import ast
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.name_parser import NameParser


# ast.Call(func, args, keywords)
# func : ast.Name이나 ast.Attribute
# args : 전달의 인자의 리스트
# keywords : 키워드별로 전달된 인수를 나타내는 키워드 개체 목록을 보유
class CallParser:
    def __init__(self, node: ast.Call, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager
        self.func = node.func
        self.args = node.args
        self.keywords = node.keywords

    def parse(self):
        func_name = self.__get_func_name()

        if func_name is 'print':
            return self.__print_parse()

    def __get_func_name(self):
        if isinstance(self.func, ast.Name):
            name_obj = NameParser(node=self.func, elem_manager=self.elem_manager).parse()
            return name_obj.id

        elif isinstance(self.func, ast.Attribute):
            raise TypeError("[call_parser] ast.Attribute는 정의되지 않았습니다.")

        else:
            raise TypeError(f"[call_parser] {type(self.func)}정의되지 않았습니다.")

    def __print_parse(self):
        for arg in self.args:
            if isinstance(arg, ast.BinOp):
                binop_obj = BinopParser(arg, self.elem_manager).parse()

        return Print(expressions=binop_obj.expressions)


@dataclass
class Print:
    expressions: list
