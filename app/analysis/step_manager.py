class StepManager:

    def __init__(self):
        self.steps = []

    def add_step(self, elem):
        self.steps.append(elem)

    def add_steps(self, elem_list: list):
        self.steps += elem_list

    def get_steps(self):
        return self.steps
