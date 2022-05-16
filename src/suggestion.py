import json


class Suggestion:
    def __init__(self, user, suggestion, date, time):
        self.user = user
        self.suggestion = suggestion
        self.date = date
        self.time = time

    @classmethod
    def from_json(cls, string):
        json_dict = json.loads(string)
        return cls(**json_dict)

    def to_json(self, path):
        with open(path, 'w') as file:
            json.dump(self, file, indent=2)
