import json
from six.moves.urllib.request import urlopen
from functools import wraps
import boto3
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError


from flask import Flask, request, jsonify, _request_ctx_stack
from flask_migrate import Migrate
from flask_cors import cross_origin, CORS
from jose import jwt
from .auth import *
from .config import Config
from .models import db
from .routes import users, songs, favorites, comments


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(users.bp)
    app.register_blueprint(songs.bp)
    app.register_blueprint(favorites.bp)
    app.register_blueprint(comments.bp)
    db.init_app(app)
    Migrate(app, db)

    # Error handler

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.route('/upload', methods=['POST'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    def upload():
        secret = os.environ.get('AWS_SECRET')
        accessKey = os.environ.get('AWS_ACCESS_KEY')
        region = os.environ.get('AWS_REGION')
        bucket = os.environ.get('AWS_BUCKET')

        s3 = boto3.client(
            "s3",
            aws_access_key_id=accessKey,
            aws_secret_access_key=secret,
        )
        try:
            file = request.files['file']
            filename = ''
            if file:
                filename = secure_filename(file.filename)
                s3.upload_fileobj(
                    file,
                    bucket,
                    filename,
                    ExtraArgs={'ACL': 'public-read'},
                )
                return jsonify(f'https://{bucket}.s3.{region}.amazonaws.com/{filename}')
        except Exception as e:
            return (str(e))

    # This doesn't need authentication

    @app.route("/api/public")
    @cross_origin(headers=["Content-Type", "Authorization"])
    def public():
        response = "Hello from a public endpoint! You don't need to be authenticated to see this."  # noqa
        return jsonify(message=response)

    # This needs authentication

    @app.route("/api/private")
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def private():
        token = request.headers.get('Authorization')
        print(token)
        response = "Hello from a private endpoint! You need to be authenticated to see this."  # noqa
        return jsonify(message=response)

    @app.route("/api/external")
    @cross_origin(headers=["Content-Type", "Authorization"])
    # @requires_auth
    def api():
        token = request.headers.get('Authorization')
        return jsonify(message=token)

    return app
