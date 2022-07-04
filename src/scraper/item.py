from dataclasses import dataclass


@dataclass
class Item:
    title: str
    link: str
    price: str
    image: str
