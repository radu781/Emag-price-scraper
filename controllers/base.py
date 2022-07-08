from configparser import ConfigParser
from aioflask import Flask
from flask_session import Session

app = Flask(__name__, template_folder="../templates", static_folder="../static")

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"
sess = Session(app)
