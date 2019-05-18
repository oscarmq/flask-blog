from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from index.models import User


class RegistrationForm(FlaskForm):

    username = StringField(label='Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField(label='Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField(label='Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])

    submit = SubmitField(label='Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This E-mail has been already taken. Please choose a different one.')


class LoginForm(FlaskForm):

    email = StringField(label='Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField(label='Password',
                             validators=[DataRequired()])

    remember = BooleanField(label='Remember Me')

    submit = SubmitField(label='Login')


class ResetPasswordRequestForm(FlaskForm):

    email = StringField(label='Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField(label='Reset Password Request')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                'There is no account for this E-mail. Please register first.')


class ResetPasswordForm(FlaskForm):

    password = PasswordField(label='Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])

    submit = SubmitField(label='Reset Password')
