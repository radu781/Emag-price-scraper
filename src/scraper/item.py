from dataclasses import dataclass, field


@dataclass
class Item:
    title: str
    link: str
    price: str
    image: str
    id_: str = field(default="-1")
    tracking: bool = field(init=False, default=False)
