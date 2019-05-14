from index import app, bcrypt, db
from flask import render_template, url_for, flash, redirect
from index.forms import RegistrationForm, LoginForm
from index.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hash_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')

        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hash_pass)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}.', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.',
                  category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
