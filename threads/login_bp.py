from functools import wraps
import bcrypt
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from threads.domainmodel.model import User
from sqlite3 import IntegrityError

login_bp = Blueprint('login', __name__)


class NameNotUniqueException(Exception):
    pass


# Registration route
@login_bp.route("/register", methods=['GET', 'POST'])
def register():
    from threads.adapters.repository import repo_instance
    form = RegistrationForm()
    error_message = None

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

            db_session = repo_instance._session_cm.session
            db_session.add(new_user)
            db_session.commit()

            success_message = 'Your account has been created! Please log in.'
            return render_template('login.html', title='Login', form=LoginForm(), success_message=success_message)
        except IntegrityError:
            db_session.rollback()
            error_message = 'Username or email already exists. Please choose another.'
        except Exception as e:
            db_session.rollback()
            error_message = 'An error occurred while creating your account.'

    return render_template('register.html', title='Register', form=form, error_message=error_message)


# Login route
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
            session['is_company'] = user.is_company
            session.permanent = True
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            error_message = 'Invalid username or password.'

    return render_template('login.html', title='Login', form=form, error_message=error_message)


@login_bp.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_company', None)  # Clear is_company from session
    return redirect(url_for('home.home'))



def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            flash(f'Login Require!', 'info')
            return redirect(url_for('login.login', next=request.url))
        from threads.adapters.repository import repo_instance
        username = session.get('username')
        user = repo_instance.get_user(username)
        if user is None or user.is_company:
            flash(f'Login Require!', 'info')
            flash(f'Need User Login!', 'info')
            return redirect(url_for('login.login', next=request.url))
        return view(**kwargs)

    return wrapped_view

def login_required_general(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            flash(f'Login Require!', 'info')
            return redirect(url_for('login.login', next=request.url))
        return view(**kwargs)
    return wrapped_view
class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, and contain an uppercase letter, a lowercase letter, and a digit.'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='Your username is required'),
                                        Length(min=2, max=20,
                                               message='Your username must be between 2 and 20 characters.')])
    email = StringField('Email', [DataRequired(message='Your email is required'),
                                  Email(message='Invalid email address.')])
    dob = DateField('Date of Birth', format='%Y-%m-%d',
                    validators=[DataRequired(message='Your date of birth is required.')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')],
                         validators=[DataRequired(message='Please select your gender.')])
    password = PasswordField('Password', [DataRequired(message='Your password is required.'), PasswordValid()])
    confirm_password = PasswordField('Confirm Password',
                                     [DataRequired(message='Please confirm your password.'),
                                      EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        from threads.adapters.repository import repo_instance
        user = repo_instance.get_user(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')


# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Your username is required.'),
                                                   Length(min=2, max=20,
                                                          message='Your username must be between 2 and 20 characters.')])
    password = PasswordField('Password', validators=[DataRequired(message='Your password is required.')])
    submit = SubmitField('Login')
