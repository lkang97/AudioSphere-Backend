from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Song, Comment

bp = Blueprint("comments", __name__, url_prefix='/songs')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('/<int:song_id>/comments')
@cross_origin(headers=["Content-Type", "Authorization"])
def get_comments(song_id):
    comments = Comment.query.filter_by(song_id=song_id).all()
    return jsonify([comment.to_dict() for comment in comments])


@bp.route('/<int:song_id>/comments', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_comment(song_id):
    data = request.json
    comment = Comment(comment=data['comment'],
                      user_id=data['user_id'],
                      song_id=data['song_id'])

    db.session.add(comment)
    db.session.commit()
    return comment.to_dict(), 201
