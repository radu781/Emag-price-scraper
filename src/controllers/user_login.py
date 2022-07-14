from aioflask import session
from flask import request, Blueprint, redirect
from models.user import User
from utils.database.user_dao import UserDAO

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
        current_user = UserDAO.log_user_in(
            User(values["user-name"], values["user-password"])
        )
        session["user_id"] = current_user.id_
        session["user_status"] = current_user.status.value
        return redirect(session["last_page"])
