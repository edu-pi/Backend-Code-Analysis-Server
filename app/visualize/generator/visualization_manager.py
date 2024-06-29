class VisualizationManager:
    def __init__(self):
        self.call_id = 0
        self.call_ids = {}
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

    def increase_depth(self):
        self.depth = self.depth + 1
        return self.depth

    def get_depth(self):
        return self.depth

    def decrease_depth(self):
        self.depth = self.depth - 1
        return self.depth