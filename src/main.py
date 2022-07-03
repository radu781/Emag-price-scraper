from itertools import count
import json
from flask import Flask, render_template, request, session, redirect, make_response
from flask_session import Session
from configparser import ConfigParser
from scraper.emag_scraper import EmagScraper
from utils.argument_parser import ArgType, Argument, ArgumentParser
from utils.dbmanager import DBManager

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = key
app.config["SESSION_TYPE"] = "SameSite"
Session(app)

db = DBManager()


@app.route("/")
def index():
    parser = ArgumentParser(
        request,
        {
            Argument("q", ArgType.Mandatory, None),
            Argument("search-count", ArgType.Optional, -1),
            Argument("price-min", ArgType.Optional, 0),
            Argument("price-max", ArgType.Optional, 10_000),
        },
    )
    values = parser.get_values()

    scraper = EmagScraper(
        "https://www.emag.ro/search/", values["q"], int(values["search-count"])
    )
    results = scraper.get_results()
    filtered = filter(
        lambda x: price_min
        <= float(
            re.sub(
                r",(\d\d) (Lei)|de la",
                r"",
                str(x["price"]),
            )
        )
        <= price_max,
        results,
    )
    sorted_res = sorted(
        filtered,
        key=lambda x: float(
            re.sub(
                r",(\d\d) (Lei)|de la",
                r"",
                str(x["price"]),
            )
        ),
    )
    response = make_response(
        render_template(
            "index.html",
            links=results[: int(values["search-count"])],
            entry_count=len(results),
            page_count=scraper.pages,
        )
    )
    return response


if __name__ == "__main__":
    app.run(port=80, debug=True)
