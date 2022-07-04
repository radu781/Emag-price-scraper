from scraper.item import Item
from utils.dbmanager import DBManager


class ItemDAO:
    @staticmethod
    def insert(item: Item) -> None:
        DBManager().execute(
            "INSERT INTO emag(title, link, image, price) values(:title, :link, :image, :price)",
            vars(item),
        )

    @staticmethod
    def insert_multiple(items: list[Item]) -> None:
        DBManager().execute_multiple(
            "INSERT INTO emag(title, link, image, price) values(:title, :link, :image, :price)",
            [vars(item) for item in items],
        )
