import ast
from dataclasses import dataclass
from typing import Optional, List

from app.analysis.element_manager import CodeElementManager


class NameParser:

    def __init__(self, node: ast.Name, elem_manager: CodeElementManager):
        self.__elem_manager = elem_manager
        self.__name_id = node.id

    @staticmethod
    def parse(node: ast.Name, elem_manager: CodeElementManager):
        name_parser = NameParser(node, elem_manager)

        if isinstance(node.ctx, ast.Load):
            value = name_parser.__get_value()
            expressions = name_parser.__get_expressions(value)
            return Name(
                id=node.id,
                value=value,
                expressions=expressions
            )

        elif isinstance(node.ctx, ast.Store):
            return Name(id=node.id)

    # 변수의 값을 가져오는 함수
    def __get_value(self):
        try:
            return self.__elem_manager.get_variable_value(name=self.__name_id)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    def __get_expressions(self, value: int):
        return [self.__name_id, str(value)]


@dataclass
class Name:
    id: str
    value: Optional[int] = None
    expressions: Optional[List[str]] = None
