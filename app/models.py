from app import db
from app import app

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True, unique=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    posts = db.relationship('Video', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'))
    title = db.Column(db.String(120), unique=False)
    video_url = db.Column(db.String(120), unique=True)
    thumbnail_url = db.Column(db.String(120), unique=False)
    likes = db.Column(db.Integer, unique=False)
    dislikes = db.Column(db.Integer, unique=False)


    def __repr__(self):
        return '<Post {}>'.format(self.body)


