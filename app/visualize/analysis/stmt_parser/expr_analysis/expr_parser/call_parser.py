from app.visualize.analysis.stmt_parser.expr_analysis.expr_util import util


class CallParser:

    @staticmethod
    def parse(func_name: str, args: list, keyword_arg_dict: dict):
        if func_name == "print":
            expressions = CallParser._print_parse(args, keyword_arg_dict)
            value = expressions[-1]
            return {"value": value, "expressions": expressions}
        elif func_name == "range":
            return CallParser._range_parse(args)

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
        identifier_list = []
        for arg in args:
            identifier_list.append(int(arg[-1]))

        return identifier_list
