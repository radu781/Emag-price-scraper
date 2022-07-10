from dataclasses import dataclass, field
from enum import Enum, auto
from hashlib import sha256


@dataclass
class User:
    class Status(Enum):
        LoggedIn = auto()
        LoggedOut = auto()
        NameMismatch = auto()
        PasswordMismatch = auto()

    name: str
    password: str | None
    id_: int = field(default=-1)
    status: Status = field(default=Status.LoggedOut)

    def __post_init__(self) -> None:
        if isinstance(self.password, str):
            self.password = sha256(bytes(self.password, "utf-8")).digest().hex()
