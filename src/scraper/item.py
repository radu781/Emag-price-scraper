from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Item:
    title: str
    link: str
    price: str
    image: str
    id_: int = field(default=-1)
    tracking: bool = field(init=False, default=False)

    @staticmethod
    def from_database_columns(columns: tuple) -> Item:
        return Item(
            str(columns[1]),
            str(columns[2]),
            str(columns[4]),
            str(columns[3]),
            int(columns[0]),
        )
