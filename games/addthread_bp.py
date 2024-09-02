import re
from flask import Blueprint, redirect, url_for, render_template,session
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime
from games.domainmodel import Thread, Tag

add_thread_bp = Blueprint('add_thread_bp', __name__)


@add_thread_bp.route('/add_thread', methods=['GET', 'POST'])
def add_thread():
    from games.adapters.repository import repo_instance
    form = ThreadContentForm()
    if form.validate_on_submit():
        # Create a new Thread object
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
            tag_name = tag_name.strip().lower()  # Normalize tag names
            tag = repo_instance.get_tag(tag_name) or Tag(tag_name)  # Fetch existing or create a new Tag
            thread.add_tag(tag)

        # Add the thread to the repository
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
