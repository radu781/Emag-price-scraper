from aioflask import session
from flask import request, Blueprint, jsonify, make_response
from flask_api import status
from models.user import User
from utils.database.user_dao import UserDAO
from flask.wrappers import Response

from utils.argument_parser import *
from . import _get_current_user

user_login_blueprint = Blueprint("user_login_blueprint", __name__)


@user_login_blueprint.route("/api/login", methods=["GET", "POST"])
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
            return make_response(
                jsonify(
                    {
                        "reason": "parameters not set: "
                        + ", ".join(arg for arg in ex.args[0])
                    }
                ),
                status.HTTP_400_BAD_REQUEST,
            )
        current_user = UserDAO.log_user_in(
            User(values["user-name"], values["user-password"])
        )
        if current_user.id_ == -1:
            return make_response(
                jsonify({"reason": User.Status.from_value(current_user.status).name}),
                status.HTTP_401_UNAUTHORIZED,
            )
        session["user_id"] = current_user.id_
        session["user_status"] = current_user.status.value
        current_user = _get_current_user(session)
        return jsonify({"user": current_user})

    return Response()
