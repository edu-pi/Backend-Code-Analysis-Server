from app.visualize.generator.convertor.for_convertor import ForConvertor


class VizConvertor:

    @staticmethod
    def convert(analyzed_stmt_list, viz_manager):
        viz_list = []
        for stmt in analyzed_stmt_list:
            if stmt.type == "assign":
                pass
            elif stmt.type == "for":
                # TODO: body로직 추가될 때 extend로변경
                viz_list.append(ForConvertor.convert(stmt, viz_manager))
            elif stmt.type == "expr":
                pass
            else:
                raise NotImplementedError(f"[VizConvertor] 지원하지 않는 노드 타입입니다.: {stmt.type}")

        return viz_list
