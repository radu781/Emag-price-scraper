import json
from controllers.user_register import register
from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response
from utils.argument_parser import *

user_register_inner_blueprint = Blueprint("user_register_inner_blueprint", __name__)


@user_register_inner_blueprint.route("/register", methods=["POST"])
def register_inner() -> Response:
    response = register()
    if response.status_code < 400:
        return make_response(jsonify({}, 200))
    return make_response(jsonify(json.loads(response.data)))
