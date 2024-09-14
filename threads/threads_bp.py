from flask import Blueprint, render_template, request
from threads.services import get_filtered_and_sorted_threads, get_sorted_tags

threads_bp = Blueprint('threads_bp', __name__)


@threads_bp.route('/threads')
def thread():
    from threads.adapters.repository import repo_instance

    page = request.args.get('page', 1, type=int)
    tag_filter = request.args.get('tag', None)
    sort_order = request.args.get('sort', 'title')

    threads_to_display, total_pages = get_filtered_and_sorted_threads(repo_instance, page, tag_filter, sort_order)
    all_tags = get_sorted_tags(repo_instance)

    return render_template(
        "threads.html",
        threads=threads_to_display,
        page=page,
        current_tag=tag_filter,
        current_sort=sort_order,
        all_tags=all_tags,
        total_pages=total_pages
    )
