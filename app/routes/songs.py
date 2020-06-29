from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, Song, User
import json
import requests

bp = Blueprint("songs", __name__, url_prefix='/songs')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Returns all the songs in the database
@bp.route('')
def get_songs():
    songs = Song.query.all()
    return jsonify([song.to_dict() for song in songs])


# Returns the information for a single song
@bp.route('/<int:song_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def single_song(song_id):
    song = Song.query.get(song_id)
    return song.to_dict(), 200


# Creates a new song
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_song():
    data = request.json
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-c-4o8wnx.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id
    song = Song(title=data['title'],
                genre=data['genre'],
                description=data['description'],
                image_url=data['image_url'],
                song_url=data['song_url'],
                user_id=userId,
                created_at=data['created_at'],
                )

    db.session.add(song)
    db.session.commit()
    return song.to_dict(), 201


# Updates a song based on its id
# @bp.route('/<int:song_id>', methods=['PATCH'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def update_song(song_id):

# Deletes a song based on id
@bp.route('/<int:song_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_song(song_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-c-4o8wnx.auth0.com/userinfo',
                       headers={'Authorization': token}).content

    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id
    song = Song.query.get(song_id)
    song_user = song.user_id
    if userId == song_user:
        db.session.delete(song)
        db.session.commit()
        return "Song has been deleted", 204
    else:
        return "Authorization denied", 401
