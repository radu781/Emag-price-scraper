from itertools import count
import json
from flask import Flask, render_template, request, session, redirect, make_response
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
    # for field in fields:
    #     if not field in request.args:
    #         return render_template("index.html")

    search_count = int(request.args.get("search-count", -1))
    price_min = int(request.args.get("price-min", 0))
    price_max = int(request.args.get("price-max", 10000))

    scraper = EmagScraper(
        "https://www.emag.ro/search/", request.args["q"], search_count
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
            links=sorted_res[:search_count],
            entry_count=len(results),
            page_count=scraper.pages,
        )
    )
    return response


if __name__ == "__main__":
    app.run(port=80, debug=True)
