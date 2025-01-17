from aioflask import session
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from utils.argument_parser import ArgType, Argument, ArgumentParser
from utils.database.item_dao import ItemDAO
from utils.price_utils import PriceUtils

from . import _get_current_user

item_page_blueprint = Blueprint("item_page_blueprint", __name__)


@item_page_blueprint.route("/api/item")
def item() -> Response:
    session["last_page"] = request.url
    parser = ArgumentParser(request, {Argument("id", ArgType.Mandatory, None)})
    values = parser.get_values()
    current_user = _get_current_user(session)

    item_id = values["id"]
    results = ItemDAO.get_all_prices(item_id)
    if results == []:
        return make_response(
            {"reason": "item id does not exist"}, status.HTTP_404_NOT_FOUND
        )
    results = PriceUtils.sieve_prices(results)
    image = ItemDAO.get_image(item_id)

    return make_response(
        jsonify({"data": results, "user": current_user, "image": image})
    )
