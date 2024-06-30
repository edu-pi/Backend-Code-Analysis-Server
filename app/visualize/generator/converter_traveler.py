from app.visualize.generator.converter.assign_converter import AssignConverter


class ConverterTraveler:

    @staticmethod
    def travel(analysis_objs):
        viz_objs = []
        for analysis_obj in analysis_objs:
            if analysis_obj.type == "assign":
                viz_objs.append(AssignConverter.convert(analysis_obj))

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {analysis_obj.type}")

        return viz_objs
