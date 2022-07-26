import json
from flask import Blueprint, make_response, jsonify
from controllers.user_login import login
from flask.wrappers import Response

from utils.argument_parser import *

user_login_inner_blueprint = Blueprint("user_login_inner_blueprint", __name__)


@user_login_inner_blueprint.route("/login", methods=["GET", "POST"])
def login_inner() -> Response:
    response = login()
    if response.status_code < 400:
        return make_response(jsonify({}), 200)
    return make_response(jsonify(json.loads(response.data)))
