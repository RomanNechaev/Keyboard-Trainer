import platform
from dataclasses import dataclass
from user import UserState


@dataclass
class User:
    state: UserState
    name: str
    os_name: str = platform.system()
