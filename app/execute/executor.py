from RestrictedPython import compile_restricted, safe_globals, PrintCollector
from RestrictedPython.Guards import guarded_setattr

from app.execute.exception.code_execute_error import CodeExecuteError
from app.execute.exception.error_enum import ErrorEnum


class Executor:
    def __init__(self, source_code: str):
        self.code = source_code

    def _get_iter(self, obj):
        """객체가 반복 가능하면 반복자를 반환."""
        if hasattr(obj, "__iter__"):
            return iter(obj)

        raise TypeError(f"{obj} is not iterable")

    def run(self):
        try:
            # 제한된 환경에서 컴파일
            byte_code = compile_restricted(self.code, filename="<string>", mode="exec")

            # 실행 환경 (globals와 locals을 제공)
            restricted_globals = safe_globals.copy()
            restricted_globals.update(
                {
                    "__builtins__": {
                        "range": range,
                        "list": list,
                        "tuple": tuple,
                        "type": type,
                        "map": map,
                        "_getattr_": getattr,
                    },  # 제한된 built-ins 사용
                    "_print_": PrintCollector,
                    "_setattr_": guarded_setattr,
                }
            )
            restricted_locals = {}
            exec(byte_code, restricted_globals, restricted_locals)
            return self._get_print_result(restricted_locals)

        except Exception as e:
            raise CodeExecuteError(ErrorEnum.CODE_EXEC_ERROR, e.args)

    def _get_print_result(self, restricted_locals):
        """_print 변수가 존재할 경우, 그 결과 반환."""
        if "_print" in restricted_locals:
            if isinstance(restricted_locals["_print"], PrintCollector):
                return "".join(restricted_locals["_print"].txt)  # 리스트 요소를 합쳐 하나의 문자열로
        return ""  # _print가 없거나 잘못된 형식일 경우 빈 문자열 반환
