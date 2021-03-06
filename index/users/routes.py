from index import bcrypt, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from index.users.forms import (
    RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm)
from index.users.utils import send_password_reset_mail
from index.models import User
from flask import Blueprint

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password.',
                  category='danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@users.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
            flash('Check your email for the instructions to reset your password.',
                  category='info')
            return redirect(url_for('users.login'))
    return render_template('reset_password_request.html', title='Reset Password Request', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('This token is invalid. Please enter your email again.',
              category='warning')
        return redirect(url_for('users.reset_password_request'))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated.',
                category='success')
            return redirect(url_for('users.login'))
        return render_template('reset_password.html', title='Reset Password', form=form)
