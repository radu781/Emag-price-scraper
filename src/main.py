import asyncio
import nest_asyncio
nest_asyncio.apply()
from aioflask import Flask, session, redirect
from flask import make_response, request,render_template
from flask_session import Session
from configparser import ConfigParser
from scraper.emag_scraper import EmagScraper
from utils.argument_parser import ArgType, Argument, ArgumentParser

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = key
app.config["SESSION_TYPE"] = "SameSite"
Session(app)


@app.route("/")
async def index():
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
    results = await asyncio.create_task(scraper.get_results())
    template = render_template(
        "index.html",
        links=results,
        page_count=scraper.pages,
    )
    response = make_response(template)
    return response


if __name__ == "__main__":
    app.run(port=80, debug=True)
