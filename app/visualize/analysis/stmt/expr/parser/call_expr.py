from app.visualize.analysis.stmt.expr.expr_util import util
from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj, RangeObj, PrintObj
from app.visualize.analysis.stmt.expr.model.range_expression import RangeExpression


class CallExpr:

    @staticmethod
    def parse(func_name: str, args: list[ExprObj], keyword_arg_dict: dict):

        if func_name == "print":
            print_expressions = CallExpr._print_parse(args, keyword_arg_dict)
            return PrintObj(value=print_expressions[-1], expressions=print_expressions)

        elif func_name == "range":
            range_iter, range_expressions = CallExpr._range_parse(args)

            return RangeObj(value=range_iter, expressions=range_expressions)

        else:
            raise TypeError(f"[CallParser]: {func_name} is not defined.")

    # ExprObj(type="print", value="abc 3\n", expressions=["abc a + 1\n", "abc 2 + 1\n", "abc 3\n"])
    @staticmethod
    def _print_parse(args: list[ExprObj], keyword_arg_dict: dict) -> tuple:
        default_keyword = {"sep": " ", "end": "\n"}
        CallExpr._apply_keywords(default_keyword, keyword_arg_dict)

        arg_expressions = [arg.expressions for arg in args]
        transposed_expressions = util.transpose_with_last_fill(arg_expressions)

        print_expressions = []

        for expressions in transposed_expressions:
            str_expression = default_keyword["sep"].join(expressions)
            print_expressions.append(str_expression + default_keyword["end"])

        return tuple(print_expressions)

    # print 함수의 키워드 파싱 : end, sep만 지원 Todo. file, flush
    @staticmethod
    def _apply_keywords(default_keyword: dict, keyword_arg_dict: dict):
        for key, value in keyword_arg_dict.items():
            default_keyword[key] = keyword_arg_dict[key]
        return default_keyword

    @staticmethod
    def _range_parse(args: list[ExprObj]) -> tuple:
        # ex ) range(a, 10, 2)
        # [
        #   ExprObj(type:name, value:3, expressions:[a, 3]},
        #   ExprObj(type:constant, value:10, expressions:[10]),
        #   ExprObj(type:constant, value:2, expressions:[2])
        # ]
        #  ->  [{start: a, end: 10, step: 2},{start: 3, end: 10, step: 2}]를 반환

        # range_iter를 만들어주는 함수
        range_iter = CallExpr._create_range_iter([arg.value for arg in args])

        # util의 transpose_with_last_fill을 이용하여 값 배열 생성
        # ['a', '10', '2'], ['3', '10', '2']
        transposed_expressions = util.transpose_with_last_fill([arg.expressions for arg in args])

        # 배열을 range_obj로 만들기
        range_expressions = [CallExpr._create_range_expression(range_list) for range_list in transposed_expressions]

        return tuple(range_iter), tuple(range_expressions)

    @staticmethod
    def _create_range_expression(range_list: list):
        if len(range_list) == 1:
            return RangeExpression(start="0", end=range_list[0], step="1")

        elif len(range_list) == 2:
            return RangeExpression(start=range_list[0], end=range_list[1], step="1")

        elif len(range_list) == 3:
            return RangeExpression(start=range_list[0], end=range_list[1], step=range_list[2])

        else:
            raise TypeError(f"[CallParser]: {range_list} 인자의 개수가 잘못되었습니다.")

    @staticmethod
    def _create_range_iter(arg_value_list: list):
        start = 0
        step = 1

        if len(arg_value_list) == 1:
            end = arg_value_list[0]

        elif len(arg_value_list) == 2:
            start = arg_value_list[0]
            end = arg_value_list[1]

        elif len(arg_value_list) == 3:
            start = arg_value_list[0]
            end = arg_value_list[1]
            step = arg_value_list[2]

        else:
            raise TypeError(f"[CallParser]: {arg_value_list} 인자의 개수가 잘못되었습니다.")

        return range(int(start), int(end), int(step))
