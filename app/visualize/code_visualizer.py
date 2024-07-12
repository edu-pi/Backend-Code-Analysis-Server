import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


# TODO 이름 수정
class CodeVisualizer:

    def __init__(self, source_code):
        self._parsed_node = ast.parse(source_code)
        self._elem_container = ElementContainer()
        self._visualization_manager = VisualizationManager()

    def visualize_code(self):
        analyzed_stmt_list = self.get_analyzed_stmt_nodes()
        return ConverterTraveler.travel(analyzed_stmt_list, self._visualization_manager)

    def get_analyzed_stmt_nodes(self):
        steps = [StmtTraveler.travel(node, self._elem_container) for node in self._parsed_node.body]

        return steps
