from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Item:
    title: str
    link: str
    price: str
    image: str
    id_: str
    tracking: bool = field(init=False, default=False)

    @staticmethod
    def from_database_columns(columns: tuple) -> Item:
        item_id = columns[0]
        return Item(
            str(columns[1]),
            str(columns[2]),
            "",
            str(columns[3]),
            item_id,
        )
