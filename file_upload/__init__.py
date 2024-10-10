from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import hashcheck


# hash cacl
hasher=hashcheck.calculate_file_hash
hashkey="static/uploads/Capture.PNG"
# Assuming `login_required` is in your main app
from auth import login_required,login_required_agent # Adjust the import if needed

# Create a blueprint for the file upload functionality
upload_bp = Blueprint('upload_bp', __name__, template_folder='templates')

# Folder to store uploaded files
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mp3'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the upload form

@upload_bp.route('/')
@login_required
@login_required_agent
def upload_form():
    return render_template('upload.html')

# Route to handle file uploads

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        if hasher(f'static/uploads/{file.filename}') == hasher(hashkey):
            session['filehash'] = True
            return redirect(url_for('progressreport'))
        else:
            return f"key doesnt exist"
    
    return "File type not allowed!"
