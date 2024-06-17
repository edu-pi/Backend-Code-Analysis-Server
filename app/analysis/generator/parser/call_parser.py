import ast
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.util import util


# ast.Call(func, args, keywords)
# func : ast.Name이나 ast.Attribute
# args : 전달의 인자의 리스트
# keywords : 키워드별로 전달된 인수를 나타내는 키워드 개체 목록을 보유
class CallParser:
    def __init__(self, node: ast.Call, elem_manager: CodeElementManager):
        self.__elem_manager = elem_manager
        self.__func = node.func
        self.__args = node.args
        self.__keywords = node.keywords

    @staticmethod
    def parse(node: ast.Call, elem_manager: CodeElementManager):
        call_parser = CallParser(node, elem_manager)
        func_name = call_parser.__get_func_name()

        if func_name == "print":
            return call_parser.__print_parse()

        elif func_name == "range":
            return call_parser.__range_parse()

        else:
            raise TypeError(f"[CallParser]: {func_name}는 정의되지 않았습니다.")

    def __get_func_name(self):
        if isinstance(self.__func, ast.Name):
            return self.__func.id

        elif isinstance(self.__func, ast.Attribute):
            raise TypeError("[call_parser] ast.Attribute는 정의되지 않았습니다.")

        else:
            raise TypeError(f"[call_parser] {type(self.__func)}정의되지 않았습니다.")

    def __print_parse(self):
        keyword_dict = self.__print_keyword_parse()
        expressions = []

        for arg in self.__args:
            if isinstance(arg, ast.BinOp):
                binop_obj = BinopParser.parse(arg, self.__elem_manager)
                expressions.append(binop_obj.expressions)

            elif isinstance(arg, ast.Name):
                name_obj = NameParser.parse(arg, self.__elem_manager)
                expressions.append(name_obj.expressions)

            elif isinstance(arg, ast.Constant):
                constant_obj = ConstantParser.parse(arg)
                expressions.append(constant_obj.expressions)

            else:
                raise TypeError(f"[call_parser] {type(arg)}는 정의되지 않았습니다.")

        transposed_expressions = util.transpose_with_last_fill(expressions)

        print_values = []
        for expressions in transposed_expressions:
            str_expression = keyword_dict["sep"].join(expressions)
            print_values.append(str_expression)

        return Print(expressions=print_values, console=print_values[-1] + keyword_dict["end"])

    # print 함수의 키워드 파싱 : end, sep만 지원 Todo. file, flush
    def __print_keyword_parse(self):
        keyword_dict = {"sep": " ", "end": "\n"}
        for keyword in self.__keywords:
            if keyword.arg == 'sep':
                constant = ConstantParser.parse(keyword.value)
                keyword_dict["sep"] = constant.value

            if keyword.arg == 'end':
                constant = ConstantParser.parse(keyword.value)
                keyword_dict["end"] = constant.value

        return keyword_dict

    def __range_parse(self):
        identifier_list = []
        for arg_node in self.__args:
            if isinstance(arg_node, ast.Name):  # 변수인 경우
                identifier = NameParser.parse(arg_node, self.__elem_manager)

            elif isinstance(arg_node, ast.Constant):  # 상수인 경우
                identifier = ConstantParser.parse(arg_node)

            elif isinstance(arg_node, ast.BinOp):  # 연산인 경우
                identifier = BinopParser.parse(arg_node, self.__elem_manager)

            else:
                raise TypeError(f"[ForGenerator]: Unsupported node type: {type(arg_node)}")

            identifier_list.append(identifier.value)

        return Range(identifier_list=identifier_list)


@dataclass
class Print:
    expressions: list
    console: str


@dataclass
class Range:
    identifier_list: list
