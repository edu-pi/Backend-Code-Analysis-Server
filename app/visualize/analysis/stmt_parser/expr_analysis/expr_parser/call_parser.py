from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_util import util


class CallParser:

    @staticmethod
    def parse(func_name: str, args: list[ExprObj], keyword_arg_dict: dict):

        if func_name == "print":
            expressions = CallParser._print_parse(args, keyword_arg_dict)
            return ExprObj(type="print", value=expressions[-1], expressions=expressions)

        elif func_name == "range":
            expressions = CallParser._range_parse(args)
            return ExprObj(type="range", value=expressions[-1], expressions=expressions)

        else:
            raise TypeError(f"[CallParser]: {func_name} is not defined.")

    # ExprObj(type="print", value="abc 3\n", expressions=["abc a + 1\n", "abc 2 + 1\n", "abc 3\n"])
    @staticmethod
    def _print_parse(args: list[ExprObj], keyword_arg_dict: dict):
        default_keyword = {"sep": " ", "end": "\n"}
        CallParser._apply_keywords(default_keyword, keyword_arg_dict)

        arg_expressions = [arg.expressions for arg in args]
        transposed_expressions = util.transpose_with_last_fill(arg_expressions)

        print_expressions = []

        for expressions in transposed_expressions:
            str_expression = default_keyword["sep"].join(expressions)
            print_expressions.append(str_expression + default_keyword["end"])

        return print_expressions

    # print 함수의 키워드 파싱 : end, sep만 지원 Todo. file, flush
    @staticmethod
    def _apply_keywords(default_keyword: dict, keyword_arg_dict: dict):
        for key, value in keyword_arg_dict.items():
            default_keyword[key] = keyword_arg_dict[key]
        return default_keyword

    @staticmethod
    def _range_parse(args: list[ExprObj]):
        # ex ) range(a, 10, 2)
        # [
        #   ExprObj(type:name, value:3, expressions:[a, 3]},
        #   ExprObj(type:constant, value:10, expressions:[10]),
        #   ExprObj(type:constant, value:2, expressions:[2])
        # ]
        #  ->  [{start: a, end: 10, step: 2},{start: 3, end: 10, step: 2}]를 반환

        # args에 있는 expressions을 꺼내와서 배열에 넣기
        expressions_list = [arg.expressions for arg in args]

        # util의 transpose_with_last_fill을 이용하여 값 배열 생성
        # ['a', '10', '2'], ['3', '10', '2']
        transposed_expressions = util.transpose_with_last_fill(expressions_list)

        # 배열을 딕셔너리로 만들기
        range_expressions = [CallParser._create_range_dict(expressions) for expressions in transposed_expressions]

        return range_expressions

    @staticmethod
    def _create_range_dict(expressions: list):
        if len(expressions) == 1:
            return {"start": "0", "end": expressions[0]}

        elif len(expressions) == 2:
            return {"start": expressions[0], "end": expressions[1]}

        elif len(expressions) == 3:
            return {"start": expressions[0], "end": expressions[1], "step": expressions[2]}

        else:
            raise TypeError(f"[CallParser]: {expressions} 인자의 개수가 잘못되었습니다.")

