from flask import Blueprint, render_template, request
from games.services import get_filtered_and_sorted_threads, get_sorted_tags

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def game():
    from games.adapters.repository import repo_instance

    page = request.args.get('page', 1, type=int)
    tag_filter = request.args.get('genre', None)
    sort_order = request.args.get('sort', 'title')

    games_to_display,total_pages= get_filtered_and_sorted_threads(repo_instance, page, tag_filter, sort_order)
    all_tags = get_sorted_tags(repo_instance)
    return render_template("games.html", games=games_to_display, page=page, current_genre=genre_filter,
                           current_sort=sort_order, all_genres=all_tags,total_pages=total_pages)
