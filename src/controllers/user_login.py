from aioflask import session
from flask import request, Blueprint, jsonify
from models.user import User
from utils.database.user_dao import UserDAO
from flask.wrappers import Response

from utils.argument_parser import *
from . import _get_current_user

user_login_blueprint = Blueprint("user_login_blueprint", __name__)


@user_login_blueprint.route("/api/login", methods=["POST"])
def login() -> Response:
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("user-name", ArgType.Mandatory, None),
                Argument("user-password", ArgType.Mandatory, None),
            },
            Method.Post,
        )
        try:
            values = parser.get_values()
        except ArgsNotFoundException as ex:
            return jsonify({"status": "fail", "unsetVariables": ex.args})
        current_user = UserDAO.log_user_in(
            User(values["user-name"], values["user-password"])
        )
        session["user_id"] = current_user.id_
        session["user_status"] = current_user.status.value
        current_user = _get_current_user(session)
        return jsonify({"status": "success", "user": current_user})

    return Response()
