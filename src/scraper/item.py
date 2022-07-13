from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(unsafe_hash=True)
class Item:
    title: str
    link: str
    price: str
    image: str
    id_: str
    tracking: bool = field(default=False)

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

    @staticmethod
    def from_dict(d: dict[str, Any]) -> Item:
        return Item(
            title=d["title"],
            link=d["link"],
            price=d["price"],
            image=d["image"],
            id_=d["id_"],
            tracking=d["tracking"],
        )
