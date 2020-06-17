from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorites_table = db.Table('favorites', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),  # noqa
        db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), nullable=False))  # noqa


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)

    songs = db.relationship('Song', back_populates='user')
    favorites = db.relationship('Song', secondary=favorites_table)


class Song(db.Model):
    __tablename = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='songs')
    favorites = db.relationship('User', secondary=favorites_table)


class Comment(db.Model):
    __tablename = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
