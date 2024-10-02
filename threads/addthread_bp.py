import re
from flask import Blueprint, redirect, url_for, render_template,session
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime
from threads.domainmodel import Thread, Tag
from threads.login_bp import login_required_general

add_thread_bp = Blueprint('add_thread_bp', __name__)


@add_thread_bp.route('/add_thread', methods=['GET', 'POST'])
@login_required_general
def add_thread():
    from threads.adapters.repository import repo_instance
    form = ThreadContentForm()
    if form.validate_on_submit():
        thread = Thread(
            thread_title=form.thread_title.data,
            thread_content=form.thread_content.data
        )
        thread.release_date = datetime.now().date()
        thread.thread_title = form.thread_title.data
        username = session.get('username')
        user = repo_instance.get_user(username)
        thread.user = user
        tag_names = form.thread_tag.data.split(',')
        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()
            tag = repo_instance.get_tag(tag_name) or Tag(tag_name)
            thread.add_tag(tag)
        repo_instance.add_thread(thread)

        return redirect(url_for('home.home'))
    return render_template('addthread.html', form=form)


def validate_hashtags(form, field):
    pattern = re.compile(r'^#\w+(, #\w+)*$')
    if not pattern.match(field.data):
        raise ValidationError('Input must be in the format "#Beauty, #Handsome".')


class ThreadContentForm(FlaskForm):
    thread_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    thread_content = StringField('Description', validators=[DataRequired()])
    thread_tag = StringField("Tag", validators=[DataRequired(message="Please Add At least One Tag"), validate_hashtags])
    submit = SubmitField('Post')
