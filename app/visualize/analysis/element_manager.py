class CodeElementManager:

    def __init__(self):
        self.call_id = 0
        self.call_ids = {}
        self.variables_value = {}
        self.depth = 0

    def get_call_id(self, node):
        if node in self.call_ids:
            return self.call_ids[node]

        new_id = self.get_next_call_id()
        self.call_ids[node] = new_id
        return new_id

    def get_next_call_id(self):
        self.call_id += 1
        return self.call_id

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

    def increase_depth(self):
        self.depth = self.depth + 1
        return self.depth

    def get_depth(self):
        return self.depth

    def decrease_depth(self):
        self.depth = self.depth - 1
        return self.depth
