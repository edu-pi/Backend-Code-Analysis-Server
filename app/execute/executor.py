from RestrictedPython import compile_restricted, safe_globals, limited_builtins, PrintCollector
from RestrictedPython.Guards import guarded_setattr

from app.execute.exception.code_execute_error import CodeExecuteError
from app.execute.exception.error_enum import ErrorEnum


class Executor:
    def __init__(self, source_code: str):
        self.code = source_code

    def run(self):
        # 제한된 환경에서 컴파일
        byte_code = compile_restricted(self.code, filename="<string>", mode="exec")

        # 실행 환경 (globals와 locals을 제공)
        restricted_globals = safe_globals.copy()
        restricted_globals.update(
            {
                "__builtins__": limited_builtins,  # 제한된 built-ins 사용
                "_print_": PrintCollector,  # print를 위한 PrintCollector 사용
                "_getattr_": guarded_setattr,
            }
        )
        restricted_locals = {}

        try:
            # 코드 실행
            exec(byte_code, restricted_globals, restricted_locals)

            # 실행 결과를 locals에서 확인
            print(restricted_locals)  # 8 출력
        except Exception as e:
            raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, e.args)
