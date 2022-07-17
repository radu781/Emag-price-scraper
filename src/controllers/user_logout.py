from aioflask import session
from flask import request, Blueprint, jsonify
from flask.wrappers import Response

from utils.argument_parser import *
from . import _get_current_user

user_logout_blueprint = Blueprint("user_logout_blueprint", __name__)


@user_logout_blueprint.route("/api/logout", methods=["POST"])
def logout() -> Response:
    if request.method == "POST":
        session.pop("user_id", None)
        session.pop("user_status", None)
        return jsonify({"user": _get_current_user(session)})

    return Response()
