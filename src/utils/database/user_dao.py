from utils.database.dbmanager import DBManager
from models.user import User


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
    def log_user_in(user: User) -> User:
        result = DBManager().execute(
            "SELECT * FROM users WHERE name=:name AND password=:password",
            {
                "name": user.name,
                "password": user.password,
            },
        )
        if result != []:
            user.id_ = int(result[0][0])
            user.status = User.Status.LoggedIn
            return user

        result = DBManager().execute(
            "SELECT * FROM users WHERE name=:name",
            {
                "name": user.name,
            },
        )
        if result != []:
            user.status = User.Status.PasswordMismatch
            return user

        user.status = User.Status.NameMismatch
        return user

    @staticmethod
    def register_user(user: User) -> None:
        DBManager().execute(
            "INSERT INTO users(name, password) VALUES(:name, :password)",
            {"name": user.name, "password": user.password},
        )

    @staticmethod
    def get_user(id_: int) -> User:
        result = DBManager().execute(
            "SELECT * FROM users WHERE id=:id",
            {
                "id": id_,
            },
        )
        return User(str(result[0][1]), None, id_, permissions=int(result[0][3]))
