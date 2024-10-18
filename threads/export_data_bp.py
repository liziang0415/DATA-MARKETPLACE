from flask import Blueprint, render_template, request, session, send_file
import pandas as pd
from io import BytesIO

export_data_bp = Blueprint('export_data_bp', __name__)


@export_data_bp.route('/export_purchased_data', methods=['GET'])
def export_purchased_data():
    from threads.adapters.repository import repo_instance
    repo = repo_instance

    # Get the user’s purchased data (customize this part according to your data model)
    user = repo.get_user(session['username'])
    purchased_threads = user.purchased_threads

    # Prepare the data for Excel (assuming purchased_threads is a list of dictionaries)
    data = []
    for thread in purchased_threads:
        tag_names = ', '.join([tag.tag_name for tag in thread.tags])
        data.append({
            'Title': thread.thread_title,
            'Content': thread.description,
            'Release Date': thread.release_date,
            'Tags': tag_names
        })

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Use a BytesIO buffer to save the Excel file in-memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Purchased Data')

    # Seek the buffer to the beginning so Flask can serve it as a file
    output.seek(0)

    # Send the file as an attachment for download
    return send_file(output, download_name="purchased_data.xlsx", as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
