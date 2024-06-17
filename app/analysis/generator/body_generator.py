import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.assign_generator import AssignGenerator
from app.analysis.generator.expr_generator import ExprGenerator
from app.analysis.generator.for_generator import ForGenerator


class BodyGenerator:

    def __init__(self, body_list, elem_manager: CodeElementManager):
        self.__body = body_list
        self.__elem_manager = elem_manager

    @staticmethod
    def generate(body: ast, elem_manager: CodeElementManager):
        body_generator = BodyGenerator(body, elem_manager)
        return body_generator.__parse_body()

    def __parse_body(self):
        self.__elem_manager.increase_depth()
        steps = []

        for node in self.__body:
            if isinstance(node, ast.Assign):
                assign_vizs = AssignGenerator.generate(node, self.__elem_manager)
                steps += assign_vizs

            elif isinstance(node, ast.For):
                for_vizs = ForGenerator.generate(node, self.__elem_manager)
                steps += for_vizs

            elif isinstance(node, ast.Expr):
                expr_vizs = ExprGenerator.generate(node, self.__elem_manager)
                steps += expr_vizs

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {type(node)}")

        self.__elem_manager.decrease_depth()

        return steps
