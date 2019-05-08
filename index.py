from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
from datetime import datetime
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)