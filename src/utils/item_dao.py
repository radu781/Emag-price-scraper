from scraper.item import Item
from utils.dbmanager import DBManager
from utils.user import User


class ItemDAO:
    @staticmethod
    def insert(item: Item) -> None:
        DBManager().execute(
            "INSERT INTO emag(title, link, image, price) VALUES(:title, :link, :image, :price)",
            vars(item),
        )

    @staticmethod
    def insert_multiple(items: list[Item]) -> None:
        DBManager().execute_multiple(
            "INSERT INTO emag(title, link, image, price) VALUES(:title, :link, :image, :price)",
            [vars(item) for item in items],
        )

    @staticmethod
    def get_matching_items(keyword: str, user: User) -> list[Item]:
        results = DBManager().execute(
            "SELECT * FROM emag WHERE title LIKE %:keyword%", {"keyword": keyword}
        )
        out: list[Item] = []
        for sub_item in results:
            out.append(Item.from_database_columns(sub_item))
        out = ItemDAO.add_tracking(out, user)
        return out

    @staticmethod
    def add_id(item: Item) -> list[Item]:
        results = DBManager().execute(
            "SELECT * FROM emag WHERE link = :link", {"link": item.link}
        )
        out: list[Item] = []
        for sub_item in results:
            out.append(Item.from_database_columns(sub_item))
        return out

    @staticmethod
    def get_tracked_items_by_user(user_id: int) -> list[Item]:
        results = DBManager().execute(
            """SELECT
                 e.id,
                 e.title,
                 e.link,
                 e.image,
                 e.price
               FROM
                 trackings AS t
                 JOIN users AS u ON t.user_id = u.id
                 AND u.id = :user_id
                 JOIN emag AS e ON e.id = t.item_id""",
            {"user_id": user_id},
        )
        out: list[Item] = []
        for item in results:
            out.append(Item(str(item[1]), item[2], item[4], item[3], item[0]))  # type: ignore
        return out

    @staticmethod
    def add_tracking(items: list[Item], user: User) -> list[Item]:
        results = ItemDAO.get_tracked_items_by_user(user.id_)
        for item in items:
            if item in results:
                item.tracking = True

        return items

    @staticmethod
    def add_tracked_item_to_user(item_id: int, user_id: int):
        DBManager().execute(
            """INSERT INTO
                 trackings(user_id, item_id)
               VALUES
               (:user_id, :item_id)""",
            {"item_id": item_id, "user_id": user_id},
        )

    @staticmethod
    def remove_tracked_item_from_user(item_id: int, user_id: int):
        DBManager().execute(
            """DELETE FROM
                  trackings AS t
                WHERE
                  t.user_id = :user_id
                  AND t.item_id = :item_id""",
            {"item_id": item_id, "user_id": user_id},
        )
