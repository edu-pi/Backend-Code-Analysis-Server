import textwrap

from RestrictedPython import compile_restricted, PrintCollector

from app.execute.exception.code_execute_error import CodeExecuteError
from app.execute.exception.code_syntax_error import CodeSyntaxError
from app.execute.exception.error_enum import ErrorEnum
from app.execute.limit_env import LimitEnv


class Executor:
    def __init__(self, source_code: str, input: str):
        self.limit_env = LimitEnv()
        self.code = textwrap.dedent(source_code)
        self.input_values = input.split("\n")
        self.cur_input_index = 0

    def execute_user_code(self):
        try:
            byte_code = compile_restricted(self.code, filename="<string>", mode="exec")

            restricted_locals = {}
            restricted_globals = self.limit_env.get_limited_globals()

            exec(byte_code, restricted_globals, restricted_locals)

            return self.get_print_result(restricted_locals)

        except SyntaxError as e:
            raise CodeSyntaxError(ErrorEnum.CODE_SYNTAX_ERROR, {"error": e.args} if e.args else {})

        except Exception as e:
            raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, {"error": e.args} if e.args else {})

    def get_print_result(self, restricted_locals):
        """_print 변수가 존재할 경우, 그 결과 반환."""
        if "_print" in restricted_locals:
            if isinstance(restricted_locals["_print"], PrintCollector):
                return "".join(restricted_locals["_print"].txt)  # 리스트 요소를 합쳐 하나의 문자열로

        return ""
