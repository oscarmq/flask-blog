from index import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from time import time
import jwt
from index.config import ConfigManager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(32), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_password_token(self, expires_in=900):
        return jwt.encode(
            {'reset_password': self.id, 'exp_time': time() + expires_in},
            key=ConfigManager.SECRET_KEY, algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, key=ConfigManager.SECRET_KEY, algorithms=['HS256'])['reset_password']
        except:
            return
        else:
            return User.query.get(id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
