from flask import render_template
from flask_login import login_required
from index.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html')
