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
