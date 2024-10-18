from flask import Blueprint, render_template, session
from .services import get_sorted_tags

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    from threads.adapters.repository import repo_instance
    recent_threads = repo_instance.get_recent_threads(limit=3)
    all_tags = get_sorted_tags(repo_instance)
    return render_template('home.html', all_tags=all_tags, recent_threads=recent_threads)
