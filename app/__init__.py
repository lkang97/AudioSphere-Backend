import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin, CORS
from jose import jwt
from .auth import *
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # Error handler

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    # This doesn't need authentication

    @app.route("/api/public")
    @cross_origin(headers=["Content-Type", "Authorization"])
    def public():
        response = "Hello from a public endpoint! You don't need to be authenticated to see this."
        return jsonify(message=response)

    # This needs authentication

    @app.route("/api/private")
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def private():
        token = request.headers.get('Authorization')
        print(token)
        response = "Hello from a private endpoint! You need to be authenticated to see this."
        return jsonify(message=response)

    return app
