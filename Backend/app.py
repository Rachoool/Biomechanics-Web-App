from flask import Flask, request, jsonify
from flask_cors import CORS
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'.stl', '.obj', '.dcm', '.nii'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file and '.' in file.filename and os.path.splitext(file.filename)[1].lower() in ALLOWED_EXTENSIONS:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"status": "success", "filename": file.filename})
    return jsonify({"status": "error", "message": "Invalid file"}), 400

if __name__ == '__main__':
    app.run(debug=True)
