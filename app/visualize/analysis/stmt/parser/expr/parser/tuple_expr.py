import ast

from app.visualize.utils.utils import Util


class TupleExpr:

    # ast.ctx가 Store인 경우엔 target_names 사용
    # ast.ctx가 Load인 경우엔 expressions 사용
    @staticmethod
    def parse(ctx: ast, elts: list):

        if isinstance(ctx, ast.Store):
            return TupleExpr._get_target_names(elts)

        elif isinstance(ctx, ast.Load):
            return TupleExpr._create_expressions(elts)

        elif isinstance(ctx, ast.Del):
            raise NotImplementedError(f"[call_travel] {type(ctx)}정의되지 않았습니다.")

        else:
            raise TypeError(f"[binop_travel] {type(ctx)}는 잘못된 타입입니다.")

    # ctx가 Store일 때 target_names를 만들어주는 함수
    @staticmethod
    def _get_target_names(elts: list):
        target_names = []

        for elt in elts:
            target_names.append(elt[-1])

        return target_names

    # ctx가 Load일 때 tuple을 계산해 value와 expression을 계산하는 함수
    @staticmethod
    def _create_expressions(elts):
        transposed_expressions = Util.transpose_with_last_fill(elts)
        tuple_expressions = list(map(tuple, transposed_expressions))

        return tuple_expressions
