class ElementContainer:

    def __init__(self):
        self.element_dict = {}

    def get_element(self, name):
        if name in self.element_dict:
            return self.element_dict[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    def set_element(self, name, value):
        if isinstance(name, tuple) and isinstance(value, tuple):
            for i in range(len(name)):
                self.element_dict[name[i]] = value[i]
            return

        self.element_dict[name] = value
        return

    def get_element_dict(self):
        return self.element_dict
