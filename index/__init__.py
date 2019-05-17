from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from index.config import ConfigManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(ConfigManager)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    from index.main.routes import main
    from index.users.routes import users
    from index.posts.routes import posts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
