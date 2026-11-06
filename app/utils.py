import os
import re
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, subfolder=''):
    """
    Saves an uploaded file to app/static/uploads/<subfolder>/
    Returns the relative path under static (e.g. 'uploads/fleets/xyz.jpg').
    """
    if not file or not hasattr(file, 'filename') or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    unique_prefix = uuid.uuid4().hex[:10]
    new_filename = f"{unique_prefix}_{filename}"

    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, new_filename)
    file.save(file_path)

    relative_path = os.path.join('uploads', subfolder, new_filename).replace('\\', '/')
    return relative_path


def generate_booking_code():
    """Generate a clean unique booking code like ASM-20261106-9A3F"""
    date_str = datetime.utcnow().strftime('%Y%m%d')
    rand_str = uuid.uuid4().hex[:4].upper()
    return f"ASM-{date_str}-{rand_str}"


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


INDONESIAN_MONTHS = [
    '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]


def format_date_id(date_val):
    if not date_val:
        return ''
    if isinstance(date_val, datetime):
        return f"{date_val.day} {INDONESIAN_MONTHS[date_val.month]} {date_val.year}"
    if hasattr(date_val, 'day'):
        return f"{date_val.day} {INDONESIAN_MONTHS[date_val.month]} {date_val.year}"
    return str(date_val)
