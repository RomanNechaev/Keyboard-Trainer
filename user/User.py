from dataclasses import dataclass, field

from typing import List

from user import UserState


@dataclass
class User:
    state: UserState
    name: str
    wpm: int = 0
    accuracy: int = 0
    mistakes: List[str] = field(default_factory=list)

    def __repr__(self):
        return f"{self.name}, {self.accuracy}, {self.wpm}"
