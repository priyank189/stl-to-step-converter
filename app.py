# File: stl_to_step_converter/app.py

import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'stl'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stl_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            step_filename = filename.rsplit('.', 1)[0] + '.step'
            step_path = os.path.join(app.config['UPLOAD_FOLDER'], step_filename)
            file.save(stl_path)

            # Run FreeCAD script to convert STL to STEP
            script_path = os.path.abspath("convert_fc.py")
            subprocess.run(["FreeCADCmd", script_path, stl_path, step_path])

            return send_file(step_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
