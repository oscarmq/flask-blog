from index import app
from flask import render_template, url_for, flash, redirect
from index.forms import RegistrationForm, LoginForm
from index.models import User, Post
from datetime import datetime

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
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'oscarmachadoquintela@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  category='danger')
    return render_template('login.html', title='Login', form=form)
