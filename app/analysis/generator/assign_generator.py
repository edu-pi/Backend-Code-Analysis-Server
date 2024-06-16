import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.generator.parser.tuple_parser import TupleParser
from app.analysis.models import AssignViz, Variable


class AssignGenerator:

    def __init__(self, node: ast.Assign, elem_manager: CodeElementManager):
        self.__targets = node.targets
        self.__value = node.value
        self.__elem_manager = elem_manager

    # ast.Assign을 assign_viz_steps으로 만들어주는 함수
    def generate(self):
        parsed_target_names = self.__parse_target_names()

        # 결과 계산 후 저장
        calculated_node = self.__calculate_node()
        for target_name in parsed_target_names:
            self.__elem_manager.add_variable_value(name=target_name, value=calculated_node["value"])

        # 표현식 변환 후 steps 생성
        assign_vizs = self.__create_assign_viz_steps(parsed_target_names, calculated_node["expressions"])

        return assign_vizs

    # ast.Assign의 속성인 Targets를 돌면서 이름을 가져오는 함수
    def __parse_target_names(self):
        target_names = []
        for target in self.__targets:
            if isinstance(target, ast.Name):
                name_obj = NameParser(target, self.__elem_manager).parse()
                target_names.append(name_obj.id)

            elif isinstance(target, ast.Tuple):
                tuple_obj = TupleParser(target, self.__elem_manager).parse()
                target_names.append(tuple_obj.target_names)

            else:
                raise TypeError(f"변수 할당에서 targets에는 다음 타입이 들어갈 수 없습니다.: {type(target)}")

        return target_names

    # ast.Assign의 속성인 value를 계산해 결과값과 표현식을 반환
    def __calculate_node(self):
        calculated_nodes = {}
        if isinstance(self.__value, ast.BinOp):
            binop_obj = BinopParser(self.__value, self.__elem_manager).parse()
            calculated_nodes["value"] = binop_obj.value
            calculated_nodes["expressions"] = binop_obj.expressions

        elif isinstance(self.__value, ast.Constant):
            constant_obj = ConstantParser(self.__value).parse()
            calculated_nodes["value"] = constant_obj.value
            calculated_nodes["expressions"] = constant_obj.expressions

        elif isinstance(self.__value, ast.Name):
            name_obj = NameParser(self.__value, self.__elem_manager).parse()
            calculated_nodes["value"] = name_obj.value
            calculated_nodes["expressions"] = name_obj.expressions

        elif isinstance(self.__value, ast.Tuple):
            tuple_obj = TupleParser(self.__value, self.__elem_manager).parse()
            calculated_nodes["value"] = tuple_obj.value
            calculated_nodes["expressions"] = tuple_obj.expressions

        else:
            raise TypeError(f"변수 할당에서 value에는 다음 타입이 들어갈 수 없습니다.: {type(self.__value)}")

        return calculated_nodes

    # parsed_target_names와 parsed_expressions를 가지고 assign_viz_steps를 만드는 함수
    def __create_assign_viz_steps(self, parsed_target_names, parsed_expressions):
        assign_vizs = []
        depth = self.__elem_manager.depth

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
