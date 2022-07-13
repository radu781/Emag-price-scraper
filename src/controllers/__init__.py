from configparser import ConfigParser
from aioflask import Flask

from utils.user import User
from utils.user_dao import UserDAO

ini_file = ConfigParser()
ini_file.read("config/data.ini")

app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
app.config["SECRET_KEY"] = ini_file.get("pages", "key")
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"


def _get_current_user(session) -> User:
    current_user = User("", None, status=User.Status.NameMismatch)
    user_id = session.get("user_id", None)
    if user_id is not None and user_id != -1:
        current_user = UserDAO.get_user(user_id)
    return current_user
