from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from index.config import ConfigManager

def create_app():
    pass


app = Flask(__name__)
app.config.from_object(ConfigManager)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from index.main.routes import main
from index.users.routes import users
from index.posts.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
