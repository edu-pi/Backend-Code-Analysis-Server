import ast

from app.analysis.generator.body_generator import BodyGenerator
from app.visualize.analysis.element_manager import CodeElementManager


# TODO 이름 수정
class CodeAnalyzer:

    def __init__(self, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager

    def visualize_code(self, parsed_ast: ast.Module):
        return BodyGenerator.generate(parsed_ast.body, self.elem_manager)
