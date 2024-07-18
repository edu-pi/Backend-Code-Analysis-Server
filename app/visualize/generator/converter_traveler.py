from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import ForStmtObj, BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.converter.expr_converter import ExprConverter
from app.visualize.generator.converter.flow_control_converter import FlowControlConverter
from app.visualize.generator.converter.for_header_converter import ForHeaderConvertor
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.visualization_manager import VisualizationManager


class ConverterTraveler:

    @staticmethod
    def travel(analysis_objs, viz_manager: VisualizationManager) -> list:
        viz_objs = []
        for analysis_obj in analysis_objs:
            if analysis_obj.type == "assign":
                viz_objs.extend(ConverterTraveler._convert_to_assign_vizs(analysis_obj, viz_manager))

            elif analysis_obj.type == "for":
                for_viz_list = ConverterTraveler._for_convert(analysis_obj, viz_manager)
                viz_objs.extend(for_viz_list)

            elif analysis_obj.type == "expr":
                viz_objs.extend(ConverterTraveler._convert_to_expr_vizs(analysis_obj, viz_manager))

            elif analysis_obj.type == "if":
                viz_objs.extend(ConverterTraveler._if_convert(analysis_obj, viz_manager))

            elif analysis_obj.type == "flowControl":
                viz_objs.append(ConverterTraveler._convert_to_flow_control_viz(analysis_obj, viz_manager))

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {analysis_obj.type}")

        return viz_objs

    @staticmethod
    def _convert_to_assign_vizs(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        steps = []
        steps.extend(ConverterTraveler._convert_to_expr_vizs(assign_obj.expr_stmt_obj, viz_manager))
        steps.append(AssignConverter.convert(assign_obj))

        return steps

    @staticmethod
    def _for_convert(for_stmt: ForStmtObj, viz_manager: VisualizationManager):
        steps = []
        # header
        header_viz = ForHeaderConvertor.convert(for_stmt, viz_manager)
        viz_manager.increase_depth()
        for body_obj in for_stmt.body_objs:
            # header step 추가
            steps.append(ForHeaderConvertor.get_updated_header(header_viz, body_obj.cur_value))
            # body step 추가
            steps.extend(ConverterTraveler.travel(body_obj.body_steps, viz_manager))
        viz_manager.decrease_depth()

        return steps

    @staticmethod
    def _if_convert(if_stmt: IfStmtObj, viz_manager: VisualizationManager):
        steps = list()
        # 1. if-else 구조 define
        steps.append(IfConverter.convert_to_if_else_define_viz(if_stmt.conditions, viz_manager))
        # 2. if header
        steps.extend(IfConverter.convert_to_if_else_change_viz(if_stmt.conditions, viz_manager))
        # 3. if header 결과 값이 true인 if 문의 body obj의 viz 생성
        if if_stmt.body_steps:
            steps.extend(ConverterTraveler._get_if_body_viz_list(if_stmt.body_steps, viz_manager))

        return steps

    @staticmethod
    def _get_if_body_viz_list(if_body_steps: list, viz_manager):
        viz_manager.increase_depth()
        body_steps_viz = ConverterTraveler.travel(if_body_steps, viz_manager)
        viz_manager.decrease_depth()

        return body_steps_viz

    @staticmethod
    def _convert_to_expr_vizs(expr_stmt_obj, viz_manager: VisualizationManager):
        return ExprConverter.convert(expr_stmt_obj, viz_manager)

    @staticmethod
    def _convert_to_flow_control_viz(flow_control_obj, viz_manager: VisualizationManager):
        flow_control_viz = FlowControlConverter.convert(flow_control_obj, viz_manager)

        return flow_control_viz
