import json


class Quiz:
    def __init__(self):
        self.category = None
        self.name = None
        self.questions = []
        self.username = None
        self.results = []

    def set_username(self, username):
        self.username = username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
