import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.assign_generator import AssignGenerator
from app.analysis.generator.expr_generator import ExprGenerator
from app.analysis.generator.for_generator import ForGenerator
from app.analysis.step_manager import StepManager


class CodeAnalyzer:

    def __init__(self, elem_manager: CodeElementManager, step_manager: StepManager):
        self.elem_manager = elem_manager
        self.step_manager = step_manager

    def visualize_code(self, parsed_ast):
        for node in parsed_ast.body:
            self.parse_node(node)
        return self.step_manager.get_steps()

    def parse_node(self, node):
        if isinstance(node, ast.Assign):
            assign_vizs = AssignGenerator.generate(node, self.elem_manager)
            self.step_manager.add_steps(assign_vizs)

        elif isinstance(node, ast.For):
            steps = ForGenerator.generate(node, self.elem_manager)
            self.step_manager.add_steps(steps)

        elif isinstance(node, ast.Expr):
            steps = ExprGenerator.generate(node, self.elem_manager)
            self.step_manager.add_steps(steps)
