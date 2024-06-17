import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.expr_generator import ExprGenerator
from app.analysis.generator.highlight.for_highlight import get_highlight_attr
from app.analysis.models import ConditionViz, ForViz
from app.analysis.generator.parser.call_parser import CallParser


class ForGenerator:
    def __init__(self, node: ast.For, elem_manager: CodeElementManager):
        self.__target = node.target
        self.__iter = node.iter
        self.__body = node.body
        self.__elem_manager = elem_manager

    @staticmethod
    def generate(node: ast.For, elem_manager: CodeElementManager):
        for_generator = ForGenerator(node, elem_manager)

        return for_generator.__create_for_viz(node, elem_manager)

    def __create_for_viz(self, node: ast.For, elem_manager):
        # Condition 객체 생성
        call_id = elem_manager.get_call_id(node)
        target_name = node.target.id
        condition = self.__create_condition_viz(target_name)

        # for문 수행
        vizs = []
        for i in range(condition.start, condition.end, condition.step):
            # target 업데이트
            elem_manager.add_variable_value(name=target_name, value=i)

            # for step 추가
            vizs.append(
                ForViz(id=call_id,
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

        if isinstance(self.__iter, ast.Call):
            range_obj = CallParser.parse(self.__iter, self.__elem_manager)
            return range_obj.identifier_list
        elif isinstance(self.__iter, ast.List):
            return
        else:
            raise TypeError(f"[ForGenerator]: Unsupported node type: {type(self.__iter)}")
