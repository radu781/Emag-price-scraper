from __future__ import annotations
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

        @staticmethod
        def from_value(value: int) -> User.Status:
            if value == User.Status.LoggedIn.value:
                return User.Status.LoggedIn
            elif value == User.Status.LoggedOut.value:
                return User.Status.LoggedOut
            elif value == User.Status.NameMismatch.value:
                return User.Status.NameMismatch
            return User.Status.PasswordMismatch

    name: str
    password: str | None
    id_: int = field(default=-1)
    status: Status = field(default=Status.LoggedOut)

    def __post_init__(self) -> None:
        if isinstance(self.password, str):
            self.password = sha256(bytes(self.password, "utf-8")).digest().hex()

    @property
    def ok(self) -> bool:
        return self.status not in [User.Status.NameMismatch, User.Status.PasswordMismatch]
