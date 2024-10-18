from flask import Blueprint, render_template, request, session
import hashlib
from threads.company_bp import company_login_required

tag_chart_bp = Blueprint('tag_chart_bp', __name__)

def get_color_for_tag(tag_name):
    hash_object = hashlib.md5(tag_name.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    r = int(hash_hex[0:2], 16)
    g = int(hash_hex[2:4], 16)
    b = int(hash_hex[4:6], 16)
    return f'rgba({r}, {g}, {b}, 1)'

@tag_chart_bp.route('/tag_chart', methods=['GET', 'POST'])
@company_login_required
def tag_chart():
    from threads.adapters.repository import repo_instance
    repo = repo_instance
    tag_data = repo.get_tag_usage_over_time()

    chart_labels = sorted(set(date['date'] for tag in tag_data.values() for date in tag))
    datasets = []
    tag_names = []

    for tag_name, data_points in tag_data.items():
        tag_names.append(tag_name)
        counts = []
        for date in chart_labels:
            count = next((point['count'] for point in data_points if point['date'] == date), 0)
            counts.append(count)

        color = get_color_for_tag(tag_name)

        datasets.append({
            'label': tag_name,
            'data': counts,
            'fill': False,
            'borderColor': color,
            'tension': 0.1
        })

    chart_data = {
        'labels': chart_labels,
        'datasets': datasets
    }

    error_message = None
    success_message = None

    if request.method == 'POST':
        selected_tag_names = request.form.getlist('tag_names')
        if not selected_tag_names:
            error_message = 'Please select at least one tag to purchase.'
            return render_template('tag_chart.html', chart_data=chart_data, tag_names=tag_names, error_message=error_message)

        # Fetch threads associated with the selected tags
        threads = repo.get_threads_by_tags(selected_tag_names)
        if not threads:
            error_message = 'No threads found for the selected tags.'
            return render_template('tag_chart.html', chart_data=chart_data, tag_names=tag_names, error_message=error_message)

        # Proceed to purchase the threads
        user = repo.get_user(session['username'])
        thread_ids = [thread.id for thread in threads]
        try:
            repo.purchase_threads(user, thread_ids)
            success_message = 'Threads purchased successfully.'
            return render_template('tag_chart.html', chart_data=chart_data, tag_names=tag_names, success_message=success_message)
        except Exception as e:
            error_message = 'An error occurred while processing your purchase.'
            return render_template('tag_chart.html', chart_data=chart_data, tag_names=tag_names, error_message=error_message)

    return render_template('tag_chart.html', chart_data=chart_data, tag_names=tag_names)

