from flask import Blueprint, render_template
from .services import get_sorted_tags

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    from threads.adapters.repository import repo_instance
    all_tags = get_sorted_tags(repo_instance)
    return render_template('home.html', all_tags=all_tags)
