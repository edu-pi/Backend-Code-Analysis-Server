import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


# TODO 이름 수정
class CodeVisualizer:

    def __init__(self, source_code):
        self._parsed_node = ast.parse(source_code)
        self._elem_manager = CodeElementManager()
        self._visualization_manager = VisualizationManager()

    def visualize_code(self):
        analyzed_stmt_list = self._analysis_parsed_node()
        return ConverterTraveler.travel(analyzed_stmt_list, self._visualization_manager)

    def _analysis_parsed_node(self):
        steps = []

        for node in self._parsed_node.body:
            if isinstance(node, ast.Assign):
                assign_obj = StmtTraveler.assign_travel(node, self._elem_manager)
                steps.append(assign_obj)

            elif isinstance(node, ast.For):
                for_vizs = StmtTraveler.for_travel(node, self._elem_manager)
                steps.append(for_vizs)

            elif isinstance(node, ast.Expr):
                expr_obj = StmtTraveler.expr_travel(node, self._elem_manager)
                steps.append(expr_obj)

            elif isinstance(node, ast.If):
                if_obj = StmtTraveler.if_travel(node, [], [], self._elem_manager)
                steps.append(if_obj)

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {type(node)}")

        return steps
