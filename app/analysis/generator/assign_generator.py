import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.generator.parser.tuple_parser import TupleParser
from app.analysis.models import AssignViz, Variable


class AssignGenerator:

    # ast.Assign을 assign_viz_steps으로 만들어주는 함수
    @staticmethod
    def generate(node: ast.Assign, elem_manager: CodeElementManager):
        parsed_target_names = AssignGenerator.__parse_target_names(node, elem_manager)

        # 결과 계산 후 저장
        calculated_node = AssignGenerator.__calculate_node(node, elem_manager)
        for target_name in parsed_target_names:
            elem_manager.add_variable_value(name=target_name, value=calculated_node["value"])

        # 표현식 변환 후 steps 생성
        assign_vizs = AssignGenerator.__create_assign_viz_steps(
            parsed_target_names,
            calculated_node["expressions"],
            elem_manager
        )

        return assign_vizs

    # ast.Assign의 속성인 Targets를 돌면서 이름을 가져오는 함수
    @staticmethod
    def __parse_target_names(node: ast.Assign, elem_manager: CodeElementManager):
        target_names = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                name_obj = NameParser.parse(target, elem_manager)
                target_names.append(name_obj.id)

            elif isinstance(target, ast.Tuple):
                tuple_obj = TupleParser.parse(target, elem_manager)
                target_names.append(tuple_obj.target_names)

            else:
                raise TypeError(f"변수 할당에서 targets에는 다음 타입이 들어갈 수 없습니다.: {type(target)}")

        return target_names

    # ast.Assign의 속성인 value를 계산해 결과값과 표현식을 반환
    @staticmethod
    def __calculate_node(node: ast.Assign, elem_manager: CodeElementManager):
        calculated_nodes = {}
        if isinstance(node.value, ast.BinOp):
            binop_obj = BinopParser.parse(node.value, elem_manager)
            calculated_nodes["value"] = binop_obj.value
            calculated_nodes["expressions"] = binop_obj.expressions

        elif isinstance(node.value, ast.Constant):
            constant_obj = ConstantParser.parse(node.value)
            calculated_nodes["value"] = constant_obj.value
            calculated_nodes["expressions"] = constant_obj.expressions

        elif isinstance(node.value, ast.Name):
            name_obj = NameParser.parse(node.value, elem_manager)
            calculated_nodes["value"] = name_obj.value
            calculated_nodes["expressions"] = name_obj.expressions

        elif isinstance(node.value, ast.Tuple):
            tuple_obj = TupleParser.parse(node.value, elem_manager)
            calculated_nodes["value"] = tuple_obj.value
            calculated_nodes["expressions"] = tuple_obj.expressions

        else:
            raise TypeError(f"변수 할당에서 value에는 다음 타입이 들어갈 수 없습니다.: {type(node.value)}")

        return calculated_nodes

    # parsed_target_names와 parsed_expressions를 가지고 assign_viz_steps를 만드는 함수
    @staticmethod
    def __create_assign_viz_steps(parsed_target_names, parsed_expressions, elem_manager: CodeElementManager):
        assign_vizs = []
        depth = elem_manager.depth

        for parsed_expression in parsed_expressions:
            # 이번 스텝에 변할 변수 리스트
            variable_vizs = []

            for target_name in parsed_target_names:
                if isinstance(parsed_expression, tuple) and isinstance(target_name, tuple):
                    for idx in range(len(target_name)):
                        variable_vizs.append(Variable(depth, str(parsed_expression[idx]), target_name[idx]))
                    continue

                variable_vizs.append(Variable(depth, str(parsed_expression), target_name))

            assign_vizs.append(AssignViz(variable_vizs))

        return assign_vizs
