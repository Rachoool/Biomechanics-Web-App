from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask import abort
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
    uploaded_files = request.files.getlist("files")  
    saved_filenames = []

    for file in uploaded_files:
        if file:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                saved_filenames.append(file.filename)

                if ext in ['.dcm', '.nii']:
                    try:
                        import SimpleITK as sitk
                        img = sitk.ReadImage(filepath)
                        vti_path = os.path.splitext(filepath)[0] + '.vti'
                        sitk.WriteImage(img, vti_path)
                        print(f"Converted to {vti_path}")
                    except Exception as e:
                        print(f"Failed to convert: {e}")

    if saved_filenames:
        return jsonify({"status": "success", "filenames": saved_filenames})
    else:
        return jsonify({"status": "error", "message": "No valid files uploaded"}), 400


@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/models')
def list_models():
    files = [
        f for f in os.listdir(app.config['UPLOAD_FOLDER'])
        if f.lower().endswith(('.stl', '.obj'))
    ]
    return jsonify({"models": files})

@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return send_from_directory(app.static_folder + '/pages', 'view_model.html')

@app.route('/api/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({"status": "success", "message": f"{filename} deleted"})
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404
    


if __name__ == '__main__':
    app.run(debug=True)
