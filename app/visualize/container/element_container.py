from app.visualize.utils import utils


class ElementContainer:

    def __init__(self, input_list: list):
        self._element_dict = {}
        self._input_list = input_list
        self._input_index = 0

    def get_element(self, name):
        if name in self._element_dict:
            return self._element_dict[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    def set_element(self, name, value):
        if utils.is_array(name) and utils.is_array(value):
            for i in range(len(name)):
                self._element_dict[name[i]] = value[i]
            return

        # 할당해야 하는 target이 리스트 의 특정 인덱스인 경우
        if "[" in name and "]" in name:
            self._set_subscript_target(name, value)
            return

        self._element_dict[name] = value
        return

    def get_element_dict(self):
        return self._element_dict

    def _set_subscript_target(self, name, value):
        # a[0:1]에서 a 추출
        list_name = name.split("[")[0]
        # a[0:1]에서 0:1 부분 추출
        sliced_index = name[name.index("[") + 1 : name.index("]")]
        # 0:1 -> [0, 1]
        slice_list = list(sliced_index.split(":"))

        # 해당 list를 찾아온다.
        find_list = self._element_dict[list_name]

        # 찾아온 list가 tuple이면 예외
        if isinstance(find_list, tuple):
            raise TypeError(f"[element container] {type(find_list)}은 수정할 수 없습니다.")

        # start, end, step 인 경우
        if len(slice_list) > 1:
            slice_list = map(int, sliced_index.split(":"))
            find_list[slice(*slice_list)] = value
            return

        # 값 하나만 바꾸는 경우
        try:
            change_idx = int(slice_list[0])  # 정수 또는 실수로 변환
        except ValueError:
            change_idx = slice_list[0]

        find_list[change_idx] = value
        return

    def get_input(self):
        if not self._input_list[self._input_index]:
            raise IndexError(f"[element_container]: input의 개수가 적습니다.")

        return_input = self._input_list[self._input_index]
        self._input_index += 1
        return return_input
