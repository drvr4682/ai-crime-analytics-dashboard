"""
backend/utils/file_handler.py
=============================
Handles file extension validations and secure saving of uploaded CSV files on disk.
"""

import os
from werkzeug.utils import secure_filename
from utils.logger import logger

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Checks if the filename has an allowed extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def save_uploaded_file(file_obj, upload_dir: str, allowed_extensions: set) -> str:
    """
    Validates and secures an uploaded file object, saving it inside upload_dir.
    Returns the absolute path to the saved file.
    """
    if not file_obj or file_obj.filename == "":
        raise ValueError("Invalid file upload object.")
        
    if not allowed_file(file_obj.filename, allowed_extensions):
        logger.warning(f"File upload blocked: Unsupported extension in '{file_obj.filename}'")
        raise ValueError("Only CSV files are allowed.")
        
    os.makedirs(upload_dir, exist_ok=True)
    filename = secure_filename(file_obj.filename)
    filepath = os.path.join(upload_dir, filename)
    
    logger.info(f"Saving uploaded file: {filename} to {filepath}")
    file_obj.save(filepath)
    return filepath
