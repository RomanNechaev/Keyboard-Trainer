from dataclasses import dataclass
from user import UserState


@dataclass
class User:
    state: UserState
    name: str
    wpm: int = 0
    accuracy: int = 0
    mistakes: int = 0
