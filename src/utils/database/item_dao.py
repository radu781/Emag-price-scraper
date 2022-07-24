import datetime
from models.item import Item
from utils.database.dbmanager import DBManager
from models.user import User
from utils.price_utils import PriceUtils


class ItemDAO:
    @staticmethod
    def insert(item: Item) -> None:
        DBManager().execute(
            "INSERT INTO emag(id, title, link, image) VALUES(:id_, :title, :link, :image)",
            vars(item),
        )

    @staticmethod
    def insert_multiple(
        items: list[Item], date: datetime.datetime
    ) -> list[dict[str, str | float]]:
        DBManager().execute_multiple(
            "INSERT INTO emag(id, title, link, image) VALUES(:id, :title, :link, :image)",
            [
                {
                    "id": item.id_,
                    "title": item.title,
                    "link": item.link,
                    "image": item.image,
                }
                for item in items
            ],
        )
        new_prices: list[dict[str, str | float]] = []
        latest_prices = ItemDAO.get_latest_prices()
        for item in items:
            for latest in latest_prices:
                if PriceUtils.price_has_updated(item, latest):
                    new_prices.append(
                        {"id": item.id_, "oldPrice": latest[3], "newPrice": item.price}
                    )

        DBManager().execute_multiple(
            "INSERT INTO prices(item_id, price, date) values(:item_id, :price, :date)",
            [
                {
                    "item_id": item.id_,
                    "price": item.price,
                    "date": str(date),
                }
                for item in items
            ],
        )
        return new_prices

    @staticmethod
    def get_matching_items(keyword: str, user: User) -> list[Item]:
        results = DBManager().execute(
            "SELECT * FROM emag WHERE title LIKE %:keyword%", {"keyword": keyword}
        )
        out: list[Item] = []
        for sub_item in results:
            out.append(ItemDAO.add_price(Item.from_database_columns(sub_item)))
        out = ItemDAO.add_tracking(out, user)
        return out

    @staticmethod
    def get_tracked_items_by_user(user_id: int) -> list[Item]:
        results = DBManager().execute(
            """SELECT * FROM (SELECT
                 e.id,
                 e.title,
                 e.link,
                 e.image,
                 p.price
               FROM
                 trackings AS t
                 JOIN users AS u ON t.user_id = u.id
                 AND u.id = :user_id
                 JOIN emag AS e ON e.id = t.item_id
                 JOIN prices AS p on p.item_id = t.item_id
               ORDER BY
                 p.date DESC) AS inn
                 GROUP BY inn.id""",
            {"user_id": user_id},
        )
        out: list[Item] = []
        for item in results:
            current_item = Item(
                title=str(item[1]),
                link=item[2],
                price=item[4],
                image=item[3],
                id_=item[0],
            )
            current_item.price = ItemDAO.get_all_prices(current_item.id_)[-1]["price"]
            out.append(current_item)
        return out

    @staticmethod
    def add_tracking(items: list[Item], user: User) -> list[Item]:
        results = ItemDAO.get_tracked_items_by_user(user.id_)
        for item in items:
            for result in results:
                if item.id_ == result.id_:
                    item.tracking = True

        return items

    @staticmethod
    def add_tracked_item_to_user(item_id: str, user_id: int):
        DBManager().execute(
            """INSERT INTO
                 trackings(user_id, item_id)
               VALUES
               (:user_id, :item_id)""",
            {"item_id": item_id, "user_id": user_id},
        )

    @staticmethod
    def remove_tracked_item_from_user(item_id: str, user_id: int):
        DBManager().execute(
            """DELETE FROM
                  trackings AS t
                WHERE
                  t.user_id = :user_id
                  AND t.item_id = :item_id""",
            {"item_id": item_id, "user_id": user_id},
        )

    @staticmethod
    def get_all_prices(item_id: str) -> list[dict[str, str]]:
        result = DBManager().execute(
            """SELECT price, date FROM prices WHERE item_id=:item_id
            ORDER BY date ASC
            """,
            {"item_id": item_id},
        )
        out: list[dict[str, str]] = []
        for item in result:
            out.append({"price": str(item[0]), "date": str(item[1])})
        return out

    @staticmethod
    def add_price(item: Item) -> Item:
        results = DBManager().execute(
            """SELECT price FROM prices WHERE item_id=:item_id ORDER BY date DESC""",
            {"item_id": item.id_},
        )
        item.price = str(results[0][0])
        return item

    @staticmethod
    def get_latest_prices() -> list[tuple]:
        return DBManager().execute(
            """SELECT
              date,
              id,
              title,
              price
            FROM
              (
                SELECT
                  e1.id,
                  e1.title,
                  p.price,
                  p.date
                FROM
                  emag AS e1
                  JOIN prices AS p on p.item_id = e1.id
                  and e1.id in (
                    SELECT
                      distinct e.id
                    FROM
                      emag AS e
                      JOIN prices AS p on p.item_id = e.id
                  )
              ) AS inner_table
            WHERE
              date in (
                SELECT
                  max(date)
                FROM
                  prices
                group by
                  item_id
              )""",
            {},
        )

    @staticmethod
    def get_image(item_id: str) -> str:
        return DBManager().execute(
            "SELECT image FROM emag WHERE id=:id", {"id": item_id}
        )[0][0]

    @staticmethod
    def get_users_tracking_item(item_id: str) -> list[str]:
        result = DBManager().execute(
            """SELECT
              user_id
            FROM
              trackings
            WHERE
              item_id = :item_id""",
            {"item_id": item_id},
        )
        return [item[0] for item in result]
