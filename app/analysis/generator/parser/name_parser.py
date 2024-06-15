import ast
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager


class NameParser:

    def __init__(self, node: ast.Name, elem_manager: CodeElementManager):
        self.__ctx = node.ctx
        self.__name_id = node.id
        self.__elem_manager = elem_manager

    def parse(self):
        if isinstance(self.__ctx, ast.Store):
            value = None
            expressions = None

        elif isinstance(self.__ctx, ast.Load):
            value = self.__get_value()
            expressions = self.__get_expressions(value)

        else:
            raise NotImplementedError(f"Unsupported node type: {type(self.__ctx)}")

        return Name(self.__name_id, value, expressions)

    # 변수의 값을 가져오는 함수
    def __get_value(self):
        try:
            return self.__elem_manager.get_variable_value(name=self.__name_id)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    def __get_expressions(self, value):
        return [self.__name_id, str(value)]


@dataclass
class Name:
    id: str
    value: int
    expressions: list
