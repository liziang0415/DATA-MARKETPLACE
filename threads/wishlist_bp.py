from flask import Blueprint, render_template, flash, redirect, session, request
from threads.login_bp import login_required
from .services import find_thread_by_title

wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route("/add/<int:thread_id>", methods=['GET'])
@login_required
def add(thread_id):
    from threads.adapters.repository import repo_instance
    username = session['username']
    thread = repo_instance.find_thread_by_id(thread_id)
    if thread:
        if repo_instance.is_in_favorite(username, thread):
            flash(f'{thread.thread_title} is already in your favorites!', 'info')
        else:
            repo_instance.add_to_favorite(username, thread)
            flash(f'{thread.thread_title} has been added to your favorites!', 'success')
    else:
        flash(f'{thread.thread_title} does not exist!', 'danger')
    return redirect(request.referrer)


@wishlist_bp.route("/remove/<string:thread_title>", methods=['GET'])
@login_required
def remove(thread_title):
    from threads.adapters.repository import repo_instance
    username = session['username']
    thread = find_thread_by_title(repo_instance, thread_title)
    if thread:
        if not repo_instance.is_in_favorite(username, thread):
            flash(f'{thread.title} is not in your favorites!', 'info')
        else:
            repo_instance.remove_from_favorite(username, thread)
            flash(f'{thread.title} has been removed from your favorites!', 'success')
    else:
        flash(f'{thread_title} does not exist!', 'danger')
    return redirect(request.referrer)


@wishlist_bp.route("/", methods=['GET'])
@login_required
def view_wishlist():
    from threads.adapters.repository import repo_instance
    username = session['username']
    favorites = repo_instance.get_favorite(username)
    if favorites is None:
        favorites = []
    return render_template('wishlist.html', favorites=favorites)
