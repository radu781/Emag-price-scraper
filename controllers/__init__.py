from configparser import ConfigParser
from aioflask import Flask

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = key
app.config["SESSION_TYPE"] = "SameSite"
app.config["SESSION_COOKIE_PATH"] = "/"
