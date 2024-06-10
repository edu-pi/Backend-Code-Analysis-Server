from unittest import TestCase
from app.analysis.highlight import expr_highlights, expr_highlight
from unittest.mock import Mock, MagicMock, call

class Test(TestCase):

    def test_expr_highlights(self):
        test_cases = [
            (["'*' * i+1", "'*' * 5", "*****"], [[], [6], [0, 1, 2, 3, 4]])
        ]

        for parsed_expr, expected_result in test_cases:
            #서브 테스크로 분리된 결과 반환
            with self.subTest(parsed_expr=parsed_expr):
                result = expr_highlights(parsed_exprs=parsed_expr)
                self.assertEqual(result, expected_result, "Valid input should highlight correct indexes.")

    def test_expr_highlight(self):
        test_cases = [
            ('a + b + 30', '10 + 20 + 30', [0, 1, 5, 6]),
            ('x * y * 5', '2 * 3 * 5', [0, 4]),
            ("'*' * 5", '*****', [0, 1, 2, 3, 4]),
            # 여기에 추가적인 테스트 케이스를 추가할 수 있습니다.
        ]

        for pre_expr, cur_expr, expected_result in test_cases:
            # 서브 테스크로 분리된 결과 반환
            with self.subTest(pre_expr=pre_expr, cur_expr=cur_expr):
                result = expr_highlight(pre_expr, cur_expr)
                self.assertEqual(result, expected_result, "Valid input should highlight correct indexes.")

