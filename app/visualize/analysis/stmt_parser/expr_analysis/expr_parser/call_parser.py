from app.visualize.analysis.stmt_parser.expr_analysis.expr_util import util


class CallParser:

    @staticmethod
    def parse(func_name: str, args: list, keyword_arg_dict: dict):

        if func_name == "print":
            expressions = CallParser._print_parse(args, keyword_arg_dict)
        elif func_name == "range":
            expressions = CallParser._range_parse(args)
        else:
            raise TypeError(f"[CallParser]: {func_name} is not defined.")

        value = expressions[-1]
        return {"value": value, "expressions": expressions}

    # ["'*' * (i + 1)\n", "'*' * (3 + 1)\n", "'****'\n"]
    @staticmethod
    def _print_parse(args: list, keyword_arg_dict: dict):
        default_keyword = {"sep": " ", "end": "\n"}
        CallParser._apply_keywords(default_keyword, keyword_arg_dict)

        transposed_expressions = util.transpose_with_last_fill(args)

        print_expressions = []

        for expressions in transposed_expressions:
            str_expression = default_keyword["sep"].join(expressions)
            print_expressions.append(str_expression + default_keyword["end"])

        return print_expressions

    # print 함수의 키워드 파싱 : end, sep만 지원 Todo. file, flush
    @staticmethod
    def _apply_keywords(default_keyword: dict, keyword_dict: dict):
        for key, value in keyword_dict.items():
            default_keyword[key] = keyword_dict[value]

    @staticmethod
    def _range_parse(args: list):
        # ex ) range(a, 10, 2)
        # [
        #   {value:3, expressions:[a, 3]},
        #   {value:10, expressions:[10]},
        #   {value:2, expressions:[2]}
        # ]
        #  ->  [{start: a, end: 10, step: 2},{start: 3, end: 10, step: 2}]를 반환

        # args에 있는 expressions을 꺼내와서 배열에 넣기
        expressions_list = [arg['expressions'] for arg in args]

        # util의 transpose_with_last_fill을 이용하여 값 배열 생성
        transposed_expressions = util.transpose_with_last_fill(expressions_list)

        # 배열을 딕셔너리로 만들기
        range_params_list = [CallParser._create_range_dict(expressions) for expressions in transposed_expressions]

        return range_params_list

    @staticmethod
    def _create_range_dict(expressions):
        range_params = {}
        if len(expressions) == 1:
            range_params['end'] = expressions[0]
        if len(expressions) >= 2:
            range_params['start'] = expressions[0]
            range_params['end'] = expressions[1]
        if len(expressions) >= 3:
            range_params['step'] = expressions[2]
        return range_params
