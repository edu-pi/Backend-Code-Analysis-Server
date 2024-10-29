import ast

from app.models.request_code import RequestCode
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler
from app.visualize.container.element_container import ElementContainer
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


class CodeVisualizer:

    def __init__(self, request_code: RequestCode):
        self._parsed_node = ast.parse(request_code.source_code)
        self._elem_container = ElementContainer(request_code.input, "main")
        self._visualization_manager = VisualizationManager(request_code.source_code)

    def visualize_code(self):
        analyzed_stmt_list = StmtTraveler.travel(self._parsed_node.body, self._elem_container)
        return ConverterTraveler.travel(analyzed_stmt_list, self._visualization_manager)
