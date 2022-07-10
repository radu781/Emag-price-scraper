from aioflask import session
from flask import request, Blueprint, redirect
from utils.user import User
from utils.user_dao import UserDAO

from utils.argument_parser import *

user_login_blueprint = Blueprint("user_login_blueprint", __name__)


@user_login_blueprint.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("user-name", ArgType.Mandatory, None),
                Argument("user-password", ArgType.Mandatory, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        user_id = UserDAO.get_user_id(User(values["user-name"], values["user-password"]))
        session["user_id"] = user_id
        return redirect("/")
