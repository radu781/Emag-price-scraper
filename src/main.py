from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from configparser import ConfigParser
import re
from scraper.emag_scraper import EmagScraper

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = key
app.config["SESSION_TYPE"] = "SameSite"
Session(app)


@app.route("/")
def index():
    fields: list[str] = ["q", "search-count", "price-min", "price-max"]
    for field in fields:
        if not field in request.args:
            return render_template("index.html")

    scraper = EmagScraper(
        "https://www.emag.ro/search/",
        request.args["q"],
        int(request.args["search-count"]),
    )

    return render_template(
        "index.html",
        links=filter(
            lambda x: int(request.args["price-min"])
            <= float(
                re.sub(
                    r",(\d\d) (Lei)",
                    r"",
                    str(x["price"]),
                )
            )
            <= int(request.args["price-max"]),
            scraper.get_results(),
        ),
    )


if __name__ == "__main__":
    app.run(port=80, debug=True)
