import ast

from app.models.request_code import RequestCode
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler
from app.visualize.container.element_container import ElementContainer
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


class CodeVisualizer:

    def __init__(self, request_code: RequestCode):
        self._parsed_node = ast.parse(request_code.source_code)
        self._elem_container = ElementContainer(request_code.input)
        self._visualization_manager = VisualizationManager(request_code.source_code)

    def visualize_code(self):
        analyzed_stmt_list = self.get_analyzed_stmt_nodes()
        return ConverterTraveler.travel(analyzed_stmt_list, self._visualization_manager)

    def get_analyzed_stmt_nodes(self):
        steps = [StmtTraveler.travel(node, self._elem_container) for node in self._parsed_node.body]

        return steps
