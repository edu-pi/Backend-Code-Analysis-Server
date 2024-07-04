class ExprHighlight:

    @staticmethod
    def get_highlight_indexes(parsed_exprs):
        highlights = []
        pre_expr = parsed_exprs[0]

        highlights.append(list(range(len(parsed_exprs[0]))))

        for cur_expr in parsed_exprs[1:-1]:
            highlights.append(ExprHighlight._immediate_expression_indices(pre_expr, cur_expr))
            pre_expr = cur_expr

        # 마지막 요소는 전체 인덱스 반환
        highlights.append(list(range(len(parsed_exprs[-1]))))

        return highlights

    # 중간 과정 중 변경된 요소에 대한 인덱스 추출
    @staticmethod
    def _immediate_expression_indices(pre_expr: str, cur_expr: str):
        highlight = []
        pre_idx = 0
        cur_idx = 0

        while cur_idx < len(cur_expr) or pre_idx < len(pre_expr):
            # 현재 인덱스가 범위를 넘지 않도록 조정
            if cur_idx < len(cur_expr) and pre_expr[pre_idx] != cur_expr[cur_idx]:
                # 이전 문자열이 끝났을 때 중단
                if pre_idx + 1 >= len(pre_expr):
                    break

                pre_idx += 1
                # 이전 문자열과 같은 요소를 찾을 때까지 변한 부분 인덱스 추가
                while cur_idx < len(cur_expr) and pre_expr[pre_idx] != cur_expr[cur_idx]:
                    # 바뀐 부분의 인덱스 추가
                    highlight.append(cur_idx)
                    cur_idx += 1
            else:
                if pre_idx < len(pre_expr):
                    pre_idx += 1
                if cur_idx < len(cur_expr):
                    cur_idx += 1

        # 남은 인덱스 추가
        while cur_idx < len(cur_expr):
            highlight.append(cur_idx)
            cur_idx += 1

        return highlight
