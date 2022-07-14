import json
from aioflask import session
from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response

from models.item import Item
from utils.argument_parser import *
from models.user import User
from utils.database.user_dao import UserDAO

from controllers.search_items import search

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index() -> Response:
    session["last_page"] = request.url
    response = await search()

    json_response = json.loads(response.data)
    try:
        data = json_response["data"]
        user = User.from_dict(json_response["user"])
        items = {Item.from_dict(data[item]) for item in data}

        return make_response(
            render_template(
                "index.html",
                links=items,
                entry_count=len(items),
                user=user,
            )
        )
    except KeyError:
        return make_response(render_template("index.html", user=None))
