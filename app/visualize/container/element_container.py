from app.visualize.utils import utils


class ElementContainer:

    def __init__(self, input_list: list, call_stack_name, input_index=0):
        self._call_stack_name = call_stack_name
        self._element_dict = {}
        self._input_list = input_list
        self._input_index = input_index

    def make_local_elem_container(self, func_name, args: dict):
        # 매개변수 개수와 들어온 값이 다른경우
        # if arg_names.length != args.length:
        #     raise ValueError("Argument length is not equal to input length")

        local_elem_container = ElementContainer(self._input_list, func_name, self._input_index)

        for var_name, var_value in self._element_dict.items():
            local_elem_container.add_element(var_name, var_value)

        # 매개변수 저장
        for arg_name, arg_value in args.items():
            local_elem_container.add_element(arg_name, arg_value)

        return local_elem_container

    def get_element(self, name):
        if name in self._element_dict:
            return self._element_dict[name]

        return None

    def add_element(self, name, value):
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

    def get_call_stack_name(self):
        return self._call_stack_name
