class StepManager:

    def __init__(self):
        self.viz_nodes = []

    def add_step(self, elem):
        self.viz_nodes.append(elem)

    def add_steps(self, elem_list: list):
        self.viz_nodes += elem_list

    def get_all_step(self):
        return self.viz_nodes
