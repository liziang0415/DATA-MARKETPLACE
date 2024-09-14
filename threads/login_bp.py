from functools import wraps
from sqlite3 import IntegrityError

import bcrypt
from flask import Blueprint, render_template, url_for, flash, redirect, session,request
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

from threads.domainmodel.model import User

login_bp = Blueprint('login', __name__)
class NameNotUniqueException(Exception):
    pass
@login_bp.route("/register", methods=['GET', 'POST'])
@login_bp.route("/register", methods=['GET', 'POST'])
def register():
    from threads.adapters.repository import repo_instance
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                username=form.username.data,
                password=hashed_password,
                email=form.email.data,
                dob=form.dob.data.strftime('%Y-%m-%d'),
                gender=form.gender.data
            )

            # Use the session directly to test
            session = repo_instance._session_cm.session
            session.add(new_user)
            session.commit()

            flash('Your account has been created!', 'success')
            return redirect(url_for('login.login'))
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            flash('An error occurred while creating your account.', 'danger')
    else:
        flash('An error occurred while creating your account.')
        print(form.errors)

    return render_template('register.html', title='Register', form=form, username_error_message=username_not_unique)


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    from threads.adapters.repository import repo_instance
    form = LoginForm()
    error_message = None

    if form.validate_on_submit():
        user = repo_instance.get_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            session['logged_in'] = True
            session['username'] = user.username
            session.permanent = True  # Optional: make the session permanent (depends on your needs)
            flash('You have been logged in!', 'success')

            # Redirect to the next page (if there's one), or home by default
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            error_message = 'Invalid username or password.'

    return render_template('login.html', title='Login', form=form, error_message=error_message)


@login_bp.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('home.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('You need to be logged in to view this page.', 'danger')
            return redirect(url_for('login.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:

    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='Your user name is required'),
                                        Length(min=2, max=20, message='Your user name is too short')])
    email = StringField('Email',
                        [DataRequired(message='Your email is required'), Email(message='Invalid email address')])
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[DataRequired(message='Your date of birth is required')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')],
                         validators=[DataRequired(message='Please select your gender')])
    password = PasswordField('Password', [DataRequired(message='Your password is required'), PasswordValid()])
    confirm_password = PasswordField('Confirm Password',
                                     [DataRequired(message='Your password is required'), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        from threads.adapters.repository import repo_instance
        user = repo_instance.get_user(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
