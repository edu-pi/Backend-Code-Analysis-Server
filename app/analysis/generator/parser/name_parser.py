import ast
from dataclasses import dataclass
from typing import Optional, List

from app.analysis.element_manager import CodeElementManager


class NameParser:
    
    @staticmethod
    def parse(node: ast.Name, elem_manager: CodeElementManager):
        if isinstance(node.ctx, ast.Load):
            value = NameParser.__get_value(elem_manager, node.id)
            expressions = NameParser.__get_expressions(node.id, value)
            return Name(node.id, value, expressions)

        elif isinstance(node.ctx, ast.Store):
            return Name(node.id)
    # 변수의 값을 가져오는 함수
    @staticmethod
    def __get_value(elem_manager: CodeElementManager, name_id: str):
        try:
            return elem_manager.get_variable_value(name=name_id)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    @staticmethod
    def __get_expressions(name_id: str, value: int):
        return [name_id, str(value)]

@dataclass
class Name:
    id: str
    value: Optional[int] = None
    expressions: Optional[List[str]] = None
