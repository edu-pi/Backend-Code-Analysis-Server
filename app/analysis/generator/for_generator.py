import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.expr_generator import ExprGenerator
from app.analysis.generator.highlight.for_highlight import get_highlight_attr
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.models import Condition, ForViz





class ForGenerator:
    def __init__(self, node: ast.For, elem_manager: CodeElementManager):
        self.value = node.value
        self.elem_manager = elem_manager

    @staticmethod
    def generate(node: ast.Assign, elem_manager: CodeElementManager):
        for_generator = ForGenerator(node, elem_manager)

        # Condition 객체 생성
        id = elem_manager.get_call_id(node)
        target_name = node.target.id
        condition = for_generator.__create_condition_viz(target_name, node.iter, elem_manager)

        # for문 수행
        vizs = []
        for i in range(condition.start, condition.end, condition.step):
            # target 업데이트
            elem_manager.add_variable_value(name=target_name, value=i)
            # for step 추가
            vizs.append(
                ForViz(id=id,
                       depth=elem_manager.get_depth(),
                       condition=condition,
                       highlight=get_highlight_attr(condition))
            )

            for_generator.__create_body_vizs(node.body, elem_manager)
            # condition 객체에서 cur 값만 변경한 새로운 condition 생성
            condition = condition.copy_with_new_cur(i + condition.step)

        return vizs

    def __create_condition_viz(self, target_name, node: ast.Call, elem_manager):
        # Condition - start, end, step
        start = 0
        end = None
        step = 1

        # args의 개수에 따라 start, end, step에 값을 할당
        identifier_list = self.__get_identifiers(elem_manager, node.args)

        if len(identifier_list) == 1:
            end = identifier_list[0]
        elif len(identifier_list) == 2:
            start, end = identifier_list
        elif len(identifier_list) == 3:
            start, end, step = identifier_list

        return Condition(target=target_name, start=start, end=end, step=step, cur=start)

    def __get_identifiers(self, elem_manager, arg_nodes):
        identifier_list = []
        for arg_node in arg_nodes:
            if isinstance(arg_node, ast.Name):
                identifier = NameParser().parse(arg_node, elem_manager)
            elif isinstance(arg_node, ast.Constant):  # 상수인 경우
                identifier = ConstantParser().parse(arg_node)
            elif isinstance(arg_node, ast.BinOp):
                identifier = BinopParser().parse(arg_node, elem_manager)
            else:
                raise TypeError(f"Unsupported node type: {type(arg_node)}")

            identifier_list.append(identifier.value)

        return identifier_list

    def __create_body_vizs(self, bodies, elem_manager):
        vizs = []
        elem_manager.increase_depth()

        for body in bodies:
            if isinstance(body, ast.Expr):
                parsed_objs = ExprGenerator.generate(body, elem_manager)
                if parsed_objs is None:
                    return vizs

                for parsed_obj in parsed_objs:
                    vizs.append(parsed_obj)

            elif isinstance(body, ast.For):
                vizs.append(ForGenerator.generate(body, elem_manager))

            else:
                raise TypeError(f"[ForGenerator]: {type(body)}은 지원하지 않습니다.")
        return vizs

    def __identifier_parse(self, node, elem_manager):
        if isinstance(node, ast.Name):  # 변수 이름인 경우
            name = NameParser().parse(node, elem_manager)
            return name.value
        elif isinstance(node, ast.Constant):  # 상수인 경우
            constant = ConstantParser().parse(node)
            return constant.value
        else:
            raise TypeError(f"Unsupported node type: {type(node)}")
