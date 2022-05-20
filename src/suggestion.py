import json
import os
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Suggestion:
    user: str = ""
    uid: int = 0
    query: str = ""
    datetime: str = ""

    @classmethod
    def from_json(cls, string):
        json_dict = json.loads(string)
        return cls(**json_dict)


def encode_suggestion(suggestion):
    if isinstance(suggestion, Suggestion):
        return {
            'user': suggestion.user,
            'uid': suggestion.uid,
            'query': suggestion.query,
            'datetime': suggestion.datetime,
        }


def to_json(suggestion, path):
    with open(path, 'a') as file:
        if os.path.getsize(path) != 0:
            file.write(',\n')
        json.dump(suggestion, file, default=encode_suggestion, indent=2)
