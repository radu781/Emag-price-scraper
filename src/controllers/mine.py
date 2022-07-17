from . import _get_current_user
from aioflask import session
from flask import make_response, jsonify, Blueprint
from flask.wrappers import Response
from utils.database.item_dao import ItemDAO

mine_blueprint = Blueprint("mine_blueprint", __name__)


@mine_blueprint.route("/api/mine", methods=["GET"])
def mine() -> Response:
    session["last_page"] = "/mine"
    current_user = _get_current_user(session)
    if current_user.id_ == -1:
        return jsonify({"status": "fail", "reason": "not logged in"})

    results = ItemDAO.get_tracked_items_by_user(current_user.id_)
    return make_response(jsonify({"data": results}))
