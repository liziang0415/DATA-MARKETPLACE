from flask import Blueprint, render_template, session

from .company_bp import company_login_required
from .login_bp import login_required_general

user_profile_bp = Blueprint('user_profile', __name__)


@user_profile_bp.route('/user_profile', methods=['GET'])
@login_required_general
def user_profile():
    from threads.adapters.repository import repo_instance
    username = session['username']
    user = repo_instance.get_user(username)

    if user.is_company:
        purchased_threads = user.purchased_threads
        return render_template('user_profile.html', user=user, purchased_threads=purchased_threads)
    else:
        reviews = user.reviews
        favorites = user.get_fav().list_of_threads if user.get_fav() else []
        threads = user.threads
        sold_threads = [thread for thread in threads if thread.sold]
        return render_template('user_profile.html', user=user, reviews=reviews, favorites=favorites,
                               sold_threads=sold_threads)

