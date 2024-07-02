class VisualizationManager:
    def __init__(self):
        self.depth = 1

    def increase_depth(self):
        self.depth = self.depth + 1
        return self.depth

    def get_depth(self):
        return self.depth

    def decrease_depth(self):
        self.depth = self.depth - 1
        return self.depth
