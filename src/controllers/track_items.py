from aioflask import session
from flask import request, Blueprint, jsonify, make_response
from flask_api import status
from utils.database.item_dao import ItemDAO
from flask.wrappers import Response
from utils.argument_parser import *
from controllers import _get_current_user

track_item_blueprint = Blueprint("track_item_blueprint", __name__)


@track_item_blueprint.route("/api/track", methods=["POST"])
def track_item() -> Response:
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("unset", ArgType.Prefix, None),
                Argument("set", ArgType.Prefix, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        current_user = _get_current_user(session)
        if current_user.ok:
            if "unset" in values:
                values["unset"] = values["unset"].replace(".x", "").replace(".y", "")
                ItemDAO.remove_tracked_item_from_user(
                    values["unset"], session["user_id"]
                )
                del values["set"]
                return jsonify({"data": values})
            elif "set" in values:
                values["set"] = values["set"].replace(".x", "").replace(".y", "")
                ItemDAO.add_tracked_item_to_user(values["set"], session["user_id"])
                return jsonify({"data": values})
            else:
                return make_response(
                    jsonify(
                        {"reason": "set or unset parameters empty"}
                    ), status.HTTP_400_BAD_REQUEST
                )
        else:
            return make_response(
                jsonify({"reason": "user not logged in"}),
                status.HTTP_401_UNAUTHORIZED,
            )
    return Response()
