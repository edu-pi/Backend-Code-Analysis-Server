class CodeElementManager:

    def __init__(self):
        self.current_id = 0
        self.variables_id = {}
        self.variables_value = {}
        self.depth = 1
        self.nodes = []

    def get_next_id(self):
        self.current_id += 1
        return self.current_id

    def get_variable_value(self, name):
        if name in self.variables_value:
            return self.variables_value[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    def add_variable_value(self, name, value):
        self.variables_value[name] = value
        return value

    def addStep(self, elem):
        self.nodes.append(elem)

    def getStep(self):
        return self.nodes

    def increase_depth(self):
        self.depth = self.depth + 1
        return self.depth

    def get_depth(self):
        return self.depth

    def decrease_depth(self):
        self.depth = self.depth - 1
        return self.depth
