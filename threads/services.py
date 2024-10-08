from datetime import datetime


def get_all_threads(repo):
    return repo.get_threads()


def get_sorted_tags(repo):
    all_tags = set()
    all_threads = repo.get_threads()
    for thread in all_threads:
        for tag in thread.tags:
            all_tags.add(tag.tag_name)
    sorted_tags = sorted(all_tags)
    return sorted_tags


def get_filtered_threads(repo, query='', tag=''):
    all_threads = repo.get_threads()
    filtered_threads = [
        thread for thread in all_threads if
        (query.lower() in thread.thread_title.lower() and
         (not tag or any(t.tag_name == tag for t in thread.tags)))
    ]
    return filtered_threads


def find_thread_by_title(repo, title: str):
    return repo.find_thread_by_title(title)


def get_filtered_and_sorted_threads(repo, page=1, tag_filter=None, sort_order='title'):
    if page < 1:
        raise ValueError("Page number must be greater than 0")

    all_threads = repo.get_threads()

    if tag_filter:
        all_threads = [thread for thread in all_threads if tag_filter in [tag.tag_name for tag in thread.tags]]

    if sort_order == 'release_date':
        all_threads.sort(
            key=lambda x: datetime.strptime(x.release_date, "%Y-%m-%d") if x.release_date else datetime.min,
            reverse=True)
    else:
        all_threads.sort(key=lambda x: x.thread_title.lower())

    per_page = 18
    offset = (page - 1) * per_page
    threads_to_display = all_threads[offset:offset + per_page]
    total_pages = (len(all_threads) + per_page - 1) // per_page

    return threads_to_display, total_pages


class NameNotUniqueException(Exception):
    pass
