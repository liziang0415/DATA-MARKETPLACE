from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from threads.domainmodel import Review
from threads.services import find_thread_by_title
from wtforms import TextAreaField, IntegerField, SubmitField

thread_description_bp = Blueprint('thread_description_bp', __name__)


@thread_description_bp.route('/threadDescription', methods=['GET', 'POST'])
def thread_description():
    from threads.adapters.repository import repo_instance
    form = ReviewForm()
    thread_id = request.args.get('thread_id')

    if not thread_id:
        return "Thread ID is missing", 400

    thread = repo_instance.find_thread_by_id(thread_id)

    if not thread:
        return "Thread not found", 404

    if form.validate_on_submit():
        username = session.get('username')
        if username:
            user = repo_instance.get_user(username)
            review = Review(user, thread, form.rating.data, form.review_text.data)
            repo_instance.add_review(review)
        return redirect(url_for('thread_description_bp.thread_description', thread_id=thread_id))

    return render_template("threadDescription.html", thread=thread, form=form)


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (0-5)', [DataRequired(), NumberRange(min=0, max=5)])
    review_text = TextAreaField('Review', [DataRequired()])
    submit = SubmitField('Submit')
