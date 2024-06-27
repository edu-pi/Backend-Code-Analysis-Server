import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler


# TODO 이름 수정
class CodeVisualizer:

    def __init__(self, source_code):
        self._parsed_node = ast.parse(source_code)
        self._elem_manager = CodeElementManager()

    def visualize_code(self):
        analysis_objs = self._analysis_parsed_node()
        # TODO: 시각화 노드 리스트 생성
        return analysis_objs

    def _analysis_parsed_node(self):
        self._elem_manager.increase_depth()
        steps = []

        for node in self._parsed_node.body:
            if isinstance(node, ast.Assign):
                assign_obj = StmtTraveler.assign_travel(node, self._elem_manager)
                # TODO:Assing_obj를 리스트가 아닌객체로 변경하고, extend -> append로 변경
                steps.extend(assign_obj)

            elif isinstance(node, ast.For):
                for_vizs = StmtTraveler.for_travel(node, self._elem_manager)
                steps.append(for_vizs)

            elif isinstance(node, ast.Expr):
                expr_obj = StmtTraveler.expr_travel(node, self._elem_manager)
                steps.append(expr_obj)

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {type(node)}")

        self._elem_manager.decrease_depth()

        return steps