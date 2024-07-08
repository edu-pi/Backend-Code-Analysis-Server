class ListHighlight:

    @staticmethod
    def get_highlight_indexes(list_exprs):
        highlights = []
        first_expr = list_exprs[0]
        is_list = first_expr[0] == "[" and first_expr[-1] == "]"

        # 처음부터 list인 경우
        if is_list:
            first_list = ListHighlight._expr_to_list(first_expr)
            highlights.append(list(range(len(first_list))))

        # name에서 list를 꺼내오는 경우
        else:
            highlights.append([0])

        # 나머지 표현식 highlight 처리
        for list_expr in list_exprs[1:]:
            cur_list = ListHighlight._expr_to_list(list_expr)
            highlights.append(list(range(len(cur_list))))

        return highlights

    @staticmethod
    def _expr_to_list(list_expr):
        return list_expr[1:-1].split(",")
