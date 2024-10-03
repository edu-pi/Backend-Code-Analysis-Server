from RestrictedPython import PrintCollector
from RestrictedPython.Guards import guarded_setattr, safe_globals

from app.execute.exception.code_execute_error import CodeExecuteError
from app.execute.exception.error_enum import ErrorEnum


class LimitEnv:
    def __init__(self):
        self._SAFE_MODULES = frozenset(("math",))

    def get_limited_globals(self):
        restricted_globals = safe_globals.copy()

        # 추가된 필드 설정
        builtins = restricted_globals.get("__builtins__")
        if builtins:
            builtins["type"] = type
            builtins["list"] = list
            builtins["map"] = map
            builtins["all"] = all
            builtins["any"] = any
            builtins["ascii"] = ascii
            builtins["bin"] = bin
            builtins["dict"] = dict
            builtins["filter"] = filter
            builtins["float"] = float
            builtins["format"] = format
            builtins["_getattr_"] = getattr
            builtins["max"] = max
            builtins["min"] = min
            builtins["set"] = set
            builtins["sum"] = sum
            builtins["super"] = super
            builtins["vars"] = vars

            builtins["input"] = self._input
            builtins["_getiter_"] = self._iter
            builtins["__import__"] = self._safe_import
            builtins["_print_"] = PrintCollector
            builtins["_setattr_"] = guarded_setattr

        return restricted_globals

    def _safe_import(self, name, *args, **kwargs):
        if name not in self._SAFE_MODULES:
            raise Exception(f"Don't you even think about {name!r}")
        return __import__(name, *args, **kwargs)

    def _iter(self, obj):
        """객체가 반복 가능하면 반복자를 반환."""
        if hasattr(obj, "__iter__"):
            return iter(obj)

    def _input(self, prompt=None):
        if self.cur_input_index < len(self.input_values):
            # prompt가 주어지면 출력 (실제로는 print가 restricted 환경에서 _print로 연결)
            if prompt:
                print(prompt, end="")  # end=""로 줄바꿈 방지

            input_value = self.input_values[self.cur_input_index]
            self.cur_input_index += 1

            return input_value
        else:
            # 더 이상 입력값이 없을 때
            raise CodeExecuteError(ErrorEnum.INPUT_SIZE_MATCHING_ERROR)
