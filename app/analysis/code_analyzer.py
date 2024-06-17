import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.body_generator import BodyGenerator


class CodeAnalyzer:

    def __init__(self, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager

    def visualize_code(self, parsed_ast: ast.Module):
        return BodyGenerator.generate(parsed_ast.body, self.elem_manager)
