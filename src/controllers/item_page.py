from utils.etc import sieve_prices
from . import _get_current_user
from aioflask import session
from flask import make_response, jsonify, Blueprint
from flask.wrappers import Response
from utils.database.item_dao import ItemDAO

item_page_blueprint = Blueprint("item_page_blueprint", __name__)


@item_page_blueprint.route("/api/item/<item_id>")
def item(item_id: str) -> Response:
    session["last_page"] = "/item"
    current_user = _get_current_user(session)
    if current_user is None:
        return make_response("broken")
    results = ItemDAO.get_all_prices(item_id)
    results = sieve_prices(results)
    image = ItemDAO.get_image(item_id)
    return make_response(
        jsonify(
            {"data": results, "user": current_user, "status": "success", "image": image}
        )
    )
