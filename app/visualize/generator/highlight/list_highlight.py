class ListHighlight:

    @staticmethod
    def get_highlight_indexes(list_exprs):
        pre_list = ListHighlight._expr_to_list(list_exprs[0])
        list_len = len(pre_list)
        highlights = [list(range(list_len))]

        for list_expr in list_exprs[1:]:
            cur_list = ListHighlight._expr_to_list(list_expr)
            highlights.append(ListHighlight._find_list_diff_idx(cur_list, pre_list))
            pre_list = cur_list

        highlights.append(list(range(list_len)))

        return highlights

    @staticmethod
    def _expr_to_list(list_expr):
        return list_expr[1:-1].split(",")

    @staticmethod
    def _find_list_diff_idx(cur_list, pre_list):
        diff_idx = []
        for idx in range(len(pre_list)):
            if pre_list[idx] != cur_list[idx]:
                diff_idx.append(idx)
        return diff_idx
