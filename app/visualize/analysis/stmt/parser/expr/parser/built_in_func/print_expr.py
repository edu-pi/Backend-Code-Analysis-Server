from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, PrintObj
from app.visualize.utils import utils


class PrintExpr:

    @staticmethod
    def parse(args: list[ExprObj], keyword_arg_dict: dict):
        key_word_dict = PrintExpr._create_keywords(keyword_arg_dict)
        expressions = PrintExpr._create_expressions(args, key_word_dict)
        value = PrintExpr._get_value(args, key_word_dict)

        return PrintObj(value=value, expressions=expressions)

        # print 함수의 키워드 파싱 : end, sep만 지원 Todo. file, flush

    @staticmethod
    def _create_keywords(keyword_arg_dict: dict):
        default_keyword = {"sep": " ", "end": "\n"}

        for key, value in keyword_arg_dict.items():
            default_keyword[key] = keyword_arg_dict[key]
        return default_keyword

    # ExprObj(type="print", value="abc 3\n", expressions=["abc a + 1\n", "abc 2 + 1\n", "abc 3\n"])
    @staticmethod
    def _create_expressions(args: list[ExprObj], key_word_dict: dict):
        arg_expressions = [arg.expressions for arg in args]
        transposed_expressions = utils.transpose_with_last_fill(arg_expressions)

        print_expressions = []

        for expressions in transposed_expressions:
            str_expression = key_word_dict["sep"].join(expressions)
            print_expressions.append(str_expression)

        return tuple(print_expressions)

    @staticmethod
    def _get_value(args: list[ExprObj], key_word_dict: dict):
        print(args)
        arg_values = [str(arg.value) for arg in args]

        str_expression = key_word_dict["sep"].join(arg_values)

        return str_expression + key_word_dict["end"]
