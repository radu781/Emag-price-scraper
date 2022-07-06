from typing import Tuple
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

    @staticmethod
    def get_all() -> list[Item]:
        return [
            Item(str(item[0]), str(item[1]), str(item[2]), str(item[4]), str(item[3]))
            for item in DBManager().execute("SELECT * FROM emag", {})
        ]

    @staticmethod
    def get_tracked_items_by_user(user_id: int) -> list[Tuple[int | str]]:
        return DBManager().execute(
            """SELECT
                 *
               FROM
                 trackings AS t
                 JOIN users AS u ON t.user_id = u.id
                 AND u.id = :user_id
                 JOIN emag ON emag.id = t.item_id""",
            {"user_id": user_id},
        )

    @staticmethod
    def add_tracked_item_to_user(item_id: int, user_id: int):
        return DBManager().execute(
            """INSERT INTO
                 trackings(user_id, item_id)
               VALUES
               (:user_id, :item_id)""",
            {"item_id": item_id, "user_id": user_id},
        )

    @staticmethod
    def add_id(item: Item) -> list[Item]:
        results = DBManager().execute(
            "SELECT * FROM emag WHERE link = :link", {"link": item.link}
        )
        out: list[Item] = []
        for item in results:
            out.append(Item(item[1], item[2], item[4], item[3], item[0]))
        return out
