from flask import Blueprint, render_template, request
from games.services import get_filtered_threads, get_sorted_tags

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    from games.adapters.repository import repo_instance
    query = request.args.get('query', '')
    tag = request.args.get('tag', '')

    filtered_threads = get_filtered_threads(repo_instance, query, tag)
    all_tags = get_sorted_tags(repo_instance)

    if not filtered_threads:
        return render_template('no_results.html'), 404

    return render_template('search_results.html', threads=filtered_threads, query=query, tag=tag, all_tags=all_tags)
