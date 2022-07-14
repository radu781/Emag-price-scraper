from aioflask import session
from flask import Blueprint, redirect, make_response
from flask.wrappers import Response
from controllers.user_logout import logout

from utils.argument_parser import *

user_logout_view_blueprint = Blueprint("user_logout_view_blueprint", __name__)


@user_logout_view_blueprint.route("/logout", methods=["POST"])
def user_logout() -> Response:
    logout()
    return make_response(redirect(session["last_page"]))
