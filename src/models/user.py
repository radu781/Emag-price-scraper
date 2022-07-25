from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto, IntEnum
from hashlib import sha256
from typing import Any


@dataclass(unsafe_hash=True)
class User:
    class Status(IntEnum):
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

    class Permission(Enum):
        RefreshSearches = 2**0

    name: str
    password: str | None
    date_created: datetime = field(default=datetime(1970, 1, 1, 0, 0, 0))
    id_: int = field(default=-1)
    status: Status = field(default=Status.LoggedIn)
    permissions: int = field(default=0)

    def __post_init__(self) -> None:
        if isinstance(self.password, str):
            self.password = sha256(bytes(self.password, "utf-8")).digest().hex()

    @property
    def ok(self) -> bool:
        return self.status not in [
            User.Status.NameMismatch,
            User.Status.PasswordMismatch,
        ]

    def has_permission(self, value: int) -> bool:
        return self.permissions & value == value

    @property
    def can_refresh(self) -> bool:
        return self.has_permission(User.Permission.RefreshSearches.value)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> User:
        return User(
            name=d["name"],
            password=d["password"],
            id_=d["id_"],
            status=d["status"],
            permissions=d["permissions"],
            date_created=d["date_created"],
        )
