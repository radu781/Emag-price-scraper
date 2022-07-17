from ast import arguments
from utils.argument_parser import ArgType, Argument, ArgumentParser
from utils.etc import sieve_prices
from . import _get_current_user
from aioflask import session
from flask import make_response, jsonify, Blueprint, request
from flask.wrappers import Response
from utils.database.item_dao import ItemDAO

item_page_blueprint = Blueprint("item_page_blueprint", __name__)


@item_page_blueprint.route("/api/item")
def item() -> Response:
    session["last_page"] = "/item"
    parser = ArgumentParser(request, {Argument("id", ArgType.Mandatory, None)})
    values = parser.get_values()
    current_user = _get_current_user(session)

    item_id = values["id"]
    results = ItemDAO.get_all_prices(item_id)
    if results == []:
        return make_response({"status": "fail", "reason": "item id does not exist"})
    results = sieve_prices(results)
    image = ItemDAO.get_image(item_id)

    return make_response(
        jsonify({"data": results, "user": current_user, "image": image})
    )
