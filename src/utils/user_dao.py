from utils.dbmanager import DBManager
from utils.user import User
from hashlib import sha256


class UserDAO:
    @staticmethod
    def insert(user: User) -> None:
        DBManager().execute(
            "INSERT INTO users(name, password) VALUES(:name, :pass)",
            {
                "name": user.name,
                "pass": user.password,
            },
        )

    @staticmethod
    def exists(user: User) -> bool:
        result = DBManager().execute(
            "SELECT * FROM users WHERE name=:name", {"name": user.name}
        )
        return len(result) > 0

    @staticmethod
    def correct_credentials(user: User) -> bool:
        result = DBManager().execute(
            "SELECT * FROM users WHERE name=:name AND password=:password",
            {
                "name": user.name,
                "password": user.password,
            },
        )
        return len(result) > 0

    @staticmethod
    def get_user_id(user: User) -> int:
        result = DBManager().execute(
            "SELECT * FROM users WHERE name=:name AND password=:password",
            {
                "name": user.name,
                "password": user.password,
            },
        )
        if result != []:
            return int(result[0][0])
        return -1

    @staticmethod
    def get_user(id_: int) -> User:
        result = DBManager().execute(
            "SELECT * FROM users WHERE id=:id",
            {
                "id": id_,
            },
        )
        return User(str(result[0][1]), None, id_)
