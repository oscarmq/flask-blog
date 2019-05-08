from flask import Flask, render_template, url_for
from datetime import datetime
app = Flask(__name__)

posts = [
    {
        'author': 'Oscar Machado',
        'title': 'Blog post 1',
        'content': 'First post',
        'day_posted': datetime.now()
    },
    {
        'author': 'Carlos Machado',
        'title': 'Blog post 1',
        'content': 'First post',
        'day_posted': datetime.now()
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)