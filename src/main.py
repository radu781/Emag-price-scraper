import asyncio
import nest_asyncio
from scraper.item import Item

nest_asyncio.apply()

from utils.item_dao import ItemDAO

from aioflask import Flask, redirect, session
from flask import make_response, render_template, request
from flask_session import Session

from configparser import ConfigParser
from scraper.emag_scraper import EmagScraper
from utils.argument_parser import ArgType, Argument, ArgumentParser, Method

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"
sess = Session(app)


@app.route("/", methods=["GET", "POST"])
async def index():
    session["user_id"] = 1
    if request.method == "GET":
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
        ItemDAO.insert_multiple(results)
        completed: list[Item] = []
        for result in results:
            for item in ItemDAO.add_id(result):
                completed.append(item)
        results = completed
        template = render_template(
            "index.html",
            links=results,
            entry_count=len(results),
        )
        response = make_response(template)
        return response
    else:
        parser = ArgumentParser(
            request, {Argument("track", ArgType.Similar, None)}, Method.Post
        )
        values = parser.get_values()
        ItemDAO.add_tracked_item_to_user(
            int(values["track"]), int(session.get("user_id", -1))
        )
        return values


@app.route("/mine")
async def mine():
    return str(ItemDAO.get_tracked_items_by_user(session.get("user_id")))


if __name__ == "__main__":
    app.run(port=80, debug=True)
