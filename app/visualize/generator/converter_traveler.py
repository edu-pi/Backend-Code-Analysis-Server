from app.visualize.analysis.stmt.model.for_stmt_obj import ForStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.convertor.for_header_convertor import ForHeaderConvertor
from app.visualize.generator.visualization_manager import VisualizationManager


class ConverterTraveler:

    @staticmethod
    def travel(analysis_objs, viz_manager):
        viz_objs = []
        for analysis_obj in analysis_objs:
            if analysis_obj.type == "assign":
                viz_objs.extend(AssignConverter.convert(analysis_obj))

            elif analysis_obj.type == "for":
                for_viz_list = ConverterTraveler._for_convert(analysis_obj, viz_manager)
                viz_objs.extend(for_viz_list)

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {analysis_obj.type}")

        return viz_objs

    @staticmethod
    def _for_convert(for_stmt: ForStmtObj, viz_manager: VisualizationManager):
        steps = []
        # header
        header_viz = ForHeaderConvertor.convert(for_stmt, viz_manager)
        for body_obj in for_stmt.body_objs:
            # header step 추가
            steps.append(ForHeaderConvertor.get_updated_header(header_viz, body_obj.cur_value))
            # body step 추가
            # steps.extend(ConverterTraveler.travel(body_obj.body_steps, viz_manager))

        return steps
