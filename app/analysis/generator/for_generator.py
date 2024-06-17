import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.expr_generator import ExprGenerator
from app.analysis.generator.highlight.for_highlight import get_highlight_attr
from app.analysis.generator.parser.binop_parser import BinopParser
from app.analysis.generator.parser.constant_parser import ConstantParser
from app.analysis.generator.parser.name_parser import NameParser
from app.analysis.models import ConditionViz, ForViz


class ForGenerator:
    def __init__(self, node: ast.For, elem_manager: CodeElementManager):
        self.__target = node.target
        self.__iter = node.iter
        self.__body = node.body
        self.__elem_manager = elem_manager

    @staticmethod
    def generate(node: ast.Assign, elem_manager: CodeElementManager):
        for_generator = ForGenerator(node, elem_manager)

        return for_generator.__create_for_viz(node, elem_manager)

    def __create_for_viz(self, node: ast.For, elem_manager):
        # Condition 객체 생성
        id = elem_manager.get_call_id(node)
        target_name = node.target.id
        condition = self.__create_condition_viz(target_name)

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
            vizs += self.__create_body_vizs()
            # condition 객체에서 cur 값만 변경한 새로운 condition 생성
            condition = condition.copy_with_new_cur(i + condition.step)

        return vizs

    def __create_condition_viz(self, target_name):
        # Condition - start, end, step
        start = 0
        end = None
        step = 1

        # args의 개수에 따라 start, end, step에 값을 할당
        identifier_list = self.__get_identifiers()

        if len(identifier_list) == 1:
            end = int(identifier_list[0])
        elif len(identifier_list) == 2:
            start, end = map(int, identifier_list)
        elif len(identifier_list) == 3:
            start, end, step = map(int, identifier_list)

        return ConditionViz(target=target_name, start=start, end=end, step=step, cur=start)

    def __create_body_vizs(self):
        "for문의 body를 파싱해서 viz 객체를 생성하는 함수"
        vizs = []
        self.__elem_manager.increase_depth()

        for body in self.__body:
            if isinstance(body, ast.Expr):
                parsed_viz = ExprGenerator.generate(body, self.__elem_manager)
                if parsed_viz is None:
                    return vizs
                elif not isinstance(parsed_viz, list):
                    raise TypeError(f"[ForGenerator]: {type(parsed_viz)}가 리스트 형식이 아닙니다.")
                else:
                    vizs += parsed_viz

            elif isinstance(body, ast.For):
                vizs += ForGenerator.generate(body, self.__elem_manager)

            else:
                raise TypeError(f"[ForGenerator]: {type(body)}은 지원하지 않습니다.")
        return vizs

    def __get_identifiers(self):
        identifier_list = []
        for arg_node in self.__iter.args:
            if isinstance(arg_node, ast.Name):  # 변수인 경우
                identifier = NameParser.parse(arg_node, self.__elem_manager)
            elif isinstance(arg_node, ast.Constant):  # 상수인 경우
                identifier = ConstantParser.parse(arg_node)
            elif isinstance(arg_node, ast.BinOp):  # 연산인 경우
                identifier = BinopParser.parse(arg_node, self.__elem_manager)
            else:
                raise TypeError(f"[ForGenerator]: Unsupported node type: {type(arg_node)}")

            identifier_list.append(identifier.value)

        return identifier_list