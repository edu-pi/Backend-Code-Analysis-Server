class CodeElementManager:

    call_id = 0
    call_ids = {}
    variables_value = {}
    depth = 1
    nodes = []

    @staticmethod
    def get_call_id(node):
        if node in CodeElementManager.call_ids:
            return CodeElementManager.call_ids[node]

        new_id = CodeElementManager.get_next_call_id()
        CodeElementManager.call_ids[node] = new_id
        return new_id

    @staticmethod
    def get_next_call_id():
        CodeElementManager.call_id += 1
        return CodeElementManager.call_id

    @staticmethod
    def get_variable_value(name):
        if name in CodeElementManager.variables_value:
            return CodeElementManager.variables_value[name]

        raise NameError(f"변수 '{name}'가 정의되지 않았습니다. ")

    @staticmethod
    def add_variable_value(name, value):
        CodeElementManager.variables_value[name] = value
        return value

    @staticmethod
    def add_step(elem):
        CodeElementManager.nodes.append(elem)

    @staticmethod
    def get_all_step():
        return CodeElementManager.nodes

    @staticmethod
    def increase_depth():
        CodeElementManager.depth = CodeElementManager.depth + 1
        return CodeElementManager.depth

    @staticmethod
    def get_depth():
        return CodeElementManager.depth

    @staticmethod
    def decrease_depth():
        CodeElementManager.depth = CodeElementManager.depth - 1
        return CodeElementManager.depth
