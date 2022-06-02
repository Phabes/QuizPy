class BasicQuestion:
    def __init__(self):
        self.question = None
        self.type = None
        self.answers = []
        self.correct = None


class ContainerQuestion:
    def __init__(self):
        self.question = None
        self.type = None
        self.containers = []
        self.answers = []


class ContainerAnswer:
    def __init__(self, text, container_id):
        self.text = text
        self.container_id = container_id
