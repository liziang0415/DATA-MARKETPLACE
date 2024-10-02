from functools import wraps
import bcrypt
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask import Blueprint, render_template, url_for, redirect, session, request
from threads.domainmodel.model import User

company_bp = Blueprint('company', __name__)

@company_bp.route("/company/register", methods=['GET', 'POST'])
def company_register():
    from threads.adapters.repository import repo_instance
    form = CompanyRegistrationForm()
    error_message = None

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_company = User(
                username=form.company_name.data,
                password=hashed_password,
                email=form.email.data,
                is_company=True
            )

            db_session = repo_instance._session_cm.session
            db_session.add(new_company)
            db_session.commit()

            success_message = 'Company account has been created successfully! Please log in.'
            return render_template('company_login.html', form=CompanyLoginForm(), success_message=success_message)
        except IntegrityError:
            db_session.rollback()
            error_message = 'Company name or email already exists. Please choose another.'
        except Exception as e:
            db_session.rollback()
            error_message = 'An error occurred while creating the company account.'

    return render_template('company_register.html', form=form, error_message=error_message)

@company_bp.route("/company/login", methods=['GET', 'POST'])
def company_login():
    from threads.adapters.repository import repo_instance
    form = CompanyLoginForm()
    error_message = None

    if form.validate_on_submit():
        company = repo_instance.get_user(form.company_name.data)
        if company and company.is_company and bcrypt.checkpw(form.password.data.encode('utf-8'), company.password.encode('utf-8')):
            session['logged_in'] = True
            session['company_logged_in'] = True
            session['username'] = company.username
            session.permanent = True
            return redirect(url_for('home.home'))
        else:
            error_message = 'Invalid company name or password.'

    return render_template('company_login.html', form=form, error_message=error_message)

@company_bp.route("/company/logout")
def company_logout():
    session.pop('logged_in', None)
    session.pop('company_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home.home'))

def company_login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        from threads.adapters.repository import repo_instance
        if not session.get('logged_in') or not session.get('company_logged_in'):
            return redirect(url_for('company.company_login', next=request.url))
        username = session.get('username')
        user = repo_instance.get_user(username)
        if not user or not user.is_company:
            return redirect(url_for('company.company_login', next=request.url))
        return view(**kwargs)
    return wrapped_view

class CompanyRegistrationForm(FlaskForm):
    company_name = StringField('Company Name', [DataRequired(message='Company name is required.'), Length(min=2, max=100, message='Company name must be between 2 and 100 characters.')])
    email = StringField('Email', [DataRequired(message='Email is required.'), Email(message='Invalid email address.')])
    password = PasswordField('Password', [DataRequired(message='Password is required.'), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', [DataRequired(message='Please confirm your password.'), EqualTo('password', message='Passwords must match.')])
    industry = StringField('Industry')
    address = StringField('Address')
    submit = SubmitField('Register')

class CompanyLoginForm(FlaskForm):
    company_name = StringField('Company Name', [DataRequired(message='Company name is required.'), Length(min=2, max=100, message='Company name must be between 2 and 100 characters.')])
    password = PasswordField('Password', [DataRequired(message='Password is required.')])
    submit = SubmitField('Login')
