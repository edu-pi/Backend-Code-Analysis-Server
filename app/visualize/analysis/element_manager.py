class CodeElementManager:

    def __init__(self):
        self.variables_value = {}

    def get_element(self, name):
        if name in self.variables_value:
            return self.variables_value[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    def set_element(self, name, value):
        if isinstance(name, tuple) and isinstance(value, tuple):
            for i in range(len(name)):
                self.variables_value[name[i]] = value[i]
            return

        self.variables_value[name] = value
        return


