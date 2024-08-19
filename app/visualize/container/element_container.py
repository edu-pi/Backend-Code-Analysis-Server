from app.visualize.utils import utils


class ElementContainer:

    def __init__(self):
        self.element_dict = {}

    def get_element(self, name):
        if name in self.element_dict:
            return self.element_dict[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    def set_element(self, name, value):
        if utils.is_array(name) and utils.is_array(value):
            for i in range(len(name)):
                self.element_dict[name[i]] = value[i]
            return

        # 할당해야 하는 target이 리스트 의 특정 인덱스인 경우
        if "[" in name and "]" in name:
            self._set_subscript_target(name, value)
            return

        self.element_dict[name] = value
        return

    def get_element_dict(self):
        return self.element_dict

    def _set_subscript_target(self, name, value):
        # a[0:1]에서 a 추출
        list_name = name.split("[")[0]
        # a[0:1]에서 0:1 부분 추출
        sliced_index = name.split("[")[1].split("]")[0]
        # 0:1 -> [0, 1]
        slice_list = [int(x) for x in sliced_index.split(":")]

        # 해당 list를 찾아온다.
        find_list = self.element_dict[list_name]

        # start, end, step 인 경우
        if len(slice_list) > 1:
            find_list[slice(*slice_list)] = value
            return

        # 값 하나만 바꾸는 경우
        find_list[int(slice_list[0])] = value
        return
