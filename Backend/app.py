from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'.stl', '.obj', '.dcm', '.nii'}

app = Flask(__name__, static_folder='../Frontend/upload', static_url_path='/upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/upload', methods=["POST"])
def upload_file():
    file = request.files.get("file")
    ext = os.path.splitext(file.filename)[1].lower()
    if file and ext in ALLOWED_EXTENSIONS:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"status": "success", "filename": file.filename})
    return jsonify({"status": "error", "message": "Invalid file"}), 400

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/models')
def list_models():
    files = []
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.lower().endswith(('.stl', '.obj')):
            files.append(f)
    return jsonify(files)

@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return send_from_directory(app.static_folder + '/pages', 'view_model.html')

if __name__ == '__main__':
    app.run(debug=True)
