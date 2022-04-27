import json


class Quiz:
    def __init__(self):
        self.category = None
        self.name = None
        self.questions = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
