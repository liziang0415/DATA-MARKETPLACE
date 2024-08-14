import re
from flask import Blueprint, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from games.domainmodel import Game

add_thread_bp = Blueprint('add_thread_bp', __name__)


@add_thread_bp.route('/add_thread', methods=['GET', 'POST'])
def add_thread():
    from games.adapters.repository import repo_instance
    form = ThreadContentForm()
    if form.validate_on_submit():
        game = Game(213, form.thread_title.data)
        repo_instance.add_game(game)
        return redirect(url_for('home.home'))
    return render_template('addthread.html', form=form)


def validate_hashtags(form, field):
    pattern = re.compile(r'^#\w+(, #\w+)*$')
    if not pattern.match(field.data):
        raise ValidationError('Input must be in the format "#Beauty, #Handsome".')


class ThreadContentForm(FlaskForm):
    thread_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200, )])
    thread_content = StringField('Description', validators=[DataRequired()])
    thread_tag = StringField("Tag", validators=[DataRequired(message="Please Add At least One Tag"), validate_hashtags])
    submit = SubmitField('Post')
