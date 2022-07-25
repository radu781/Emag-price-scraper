from aioflask import session
from flask import request, Blueprint, jsonify, make_response
from flask_api import status
from mail.welcome_email import WelcomeEmail
from models.user import User
from utils.database.user_dao import UserDAO
from flask.wrappers import Response
from mail.sender import EmailSender

from utils.argument_parser import *
from . import _get_current_user

user_register_blueprint = Blueprint("user_register_blueprint", __name__)


@user_register_blueprint.route("/api/register", methods=["POST"])
def register() -> Response:
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("user-name", ArgType.Mandatory, None),
                Argument("user-password", ArgType.Mandatory, None),
                Argument("user-password-confirm", ArgType.Mandatory, None),
            },
            Method.Post,
        )
        try:
            values = parser.get_values()
        except ArgsNotFoundException as ex:
            return make_response(
                jsonify({"unsetVariables": ex.args}),
                status.HTTP_400_BAD_REQUEST,
            )
        if values["user-password"] != values["user-password-confirm"]:
            return make_response(
                jsonify({"reason": "passwords are not the same"}),
                status.HTTP_400_BAD_REQUEST,
            )
        current_user = User(values["user-name"], values["user-password"])
        if UserDAO.exists(current_user):
            return make_response(
                jsonify({"reason": "user already exists"}),
                status.HTTP_400_BAD_REQUEST,
            )

        UserDAO.register_user(current_user)
        UserDAO.log_user_in(current_user)
        EmailSender.queue(WelcomeEmail(current_user))

        session["user_id"] = current_user.id_
        session["user_status"] = current_user.status.value
        current_user = _get_current_user(session)
        return jsonify({"user": current_user})

    return Response()
