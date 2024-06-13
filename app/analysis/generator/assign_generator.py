import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.models import AssignViz, Variable


class AssignGenerator:

    def __init__(self, node: ast.Assign, elem_manager: CodeElementManager):
        self.node = node
        self.elem_manager = elem_manager

    # ast.Assign을 assign_viz_steps으로 만들어주는 함수
    def generate(self):
        parsed_target_names = self.__parse_target_names()
        parsed_expressions = self.__parse_value_to_expressions()

        for target_name in parsed_target_names:
            self.elem_manager.add_variable_value(name=target_name, value=parsed_expressions[-1])

        # elem 저장
        assign_viz_steps = self.__create_assign_viz_steps(parsed_target_names, parsed_expressions)

        return assign_viz_steps

    # ast.Assign의 속성인 Targets를 돌면서 이름을 가져오는 함수
    def __parse_target_names(self):
        target_names = []
        for target in self.node.targets:
            if isinstance(target, ast.Name):
                target_names.append(target.id)

            else:
                raise TypeError(f"변수 할당에서 targets에는 다음 타입이 들어갈 수 없습니다.: {type(target)}")

        return target_names

    # ast.Assign의 속성인 value를 표현식으로 가져오는 함수
    def __parse_value_to_expressions(self):
        parsed_expressions = []
        assign_value = self.node.value

        if isinstance(assign_value, ast.BinOp):
            binop = BinopParser(assign_value, self.elem_manager).parse()
            parsed_expressions += binop.expressions

        elif isinstance(assign_value, ast.Constant):
            constant = ConstantParser(assign_value).parse()
            parsed_expressions.append(constant.value)

        elif isinstance(assign_value, ast.Name):
            name = NameParser(assign_value, self.elem_manager).parse()
            parsed_expressions += name.expressions

        else:
            raise TypeError(f"변수 할당에서 value에는 다음 타입이 들어갈 수 없습니다.: {type(assign_value)}")

        return parsed_expressions

    # parsed_target_names와 parsed_expressions를 가지고 assign_viz_steps를 만드는 함수
    def __create_assign_viz_steps(self, parsed_target_names, parsed_expressions):
        assign_viz_steps = []
        depth = self.elem_manager.depth

        for parsed_expression in parsed_expressions:
            # 이번 스텝에 변할 변수 리스트
            assign_variables = []

            for target_name in parsed_target_names:
                assign_variables.append(Variable(depth, str(parsed_expression), target_name))

            assign_viz_steps.append(AssignViz(assign_variables))

        return assign_viz_steps
