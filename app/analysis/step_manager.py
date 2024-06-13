class StepManager:

    def __init__(self):
        self.nodes = []

    def add_step(self, elem):
        self.nodes.append(elem)

    def add_steps(self, elem_list: list):
        self.nodes += elem_list

    def get_all_step(self):
        return self.nodes
