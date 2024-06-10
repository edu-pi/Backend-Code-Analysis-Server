from unittest import TestCase
from unittest.mock import patch
from app.analysis.highlight import expressions_highlight_indices, immediate_expression_indices


class HighlightTest(TestCase):
    @patch('app.analysis.highlight.expr_highlight')
    def test_expr_highlights(self, mock_expr_highlight):
        # given
        test_cases = [
            (["'*' * i+1", "'*' * 5", "*****"], [[], [6], [0, 1, 2, 3, 4]])
        ]
        # expr_highlight 함수를 목업으로 테스트
        mock_expr_highlight.side_effect = lambda expr1, expr2: {
            ("'*' * i+1", "'*' * i+1"): [],
            ("'*' * i+1", "'*' * 5"): [6],
            ("'*' * 5", "*****"): [0, 1, 2, 3, 4]
        }.get((expr1, expr2), [])

        # when
        for parsed_expr, expected_result in test_cases:
            # 서브 테스크로 분리된 결과 반환
            with self.subTest(parsed_expr=parsed_expr):
                result = expressions_highlight_indices(parsed_exprs=parsed_expr)
                # then
                self.assertEqual(result, expected_result)

    def test_expr_highlight(self):
        # given
        test_cases = [

            ("'x' * 5", 'xxxxx', [0, 1, 2, 3, 4])
        ]

        for pre_expr, cur_expr, expected_result in test_cases:
            # then
            with self.subTest(pre_expr=pre_expr, cur_expr=cur_expr):
                result = immediate_expression_indices(pre_expr, cur_expr)
                # when
                self.assertEqual(result, expected_result, "Valid input should highlight correct indexes.")
