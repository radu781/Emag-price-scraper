from dataclasses import dataclass, field
from hashlib import sha256


@dataclass
class User:
    name: str
    password: str
    id_: int = field(default=-1)

    def __post_init__(self):
        self.password = sha256(bytes(self.password, "utf-8")).digest().hex()
