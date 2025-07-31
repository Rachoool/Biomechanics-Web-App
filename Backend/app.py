from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask import abort
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'.stl', '.obj', '.dcm', '.nii'}

FRONTEND_DIR = os.path.join(BASE_DIR, 'Frontend', 'upload')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='/upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("STATIC DIR:", app.static_folder)
print("Expected index path:", os.path.join(app.static_folder, 'pages', 'view_Model.html'))


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/upload', methods=["POST"])
def upload_file():
    uploaded_files = request.files.getlist("files")  
    print(f"[Upload] Received {len(uploaded_files)} file(s).")  

    saved_filenames = []

    for file in uploaded_files:
        if file:
            ext = os.path.splitext(file.filename)[1].lower()
            print(f"[Upload] Processing file: {file.filename} with extension: {ext}")  

            if ext in ALLOWED_EXTENSIONS:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                saved_filenames.append(file.filename)
                print(f"[Upload] Saved file to: {filepath}")  

                if ext in ['.dcm', '.nii']:
                    try:
                        import SimpleITK as sitk
                        img = sitk.ReadImage(filepath)
                        vti_path = os.path.splitext(filepath)[0] + '.vti'
                        sitk.WriteImage(img, vti_path)
                        print(f"[Convert] Successfully converted to: {vti_path}")  
                    except Exception as e:
                        print(f"[Error] Conversion failed for {file.filename}: {e}")  

            else:
                print(f"[Warning] Skipped unsupported file type: {file.filename}")  

    if saved_filenames:
        print(f"[Upload] Upload completed. Files: {saved_filenames}")  
        return jsonify({"status": "success", "filenames": saved_filenames})
    else:
        print("[Upload] No valid files uploaded.")  
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
    return send_from_directory(os.path.join(app.static_folder, 'pages'), 'index.html')


@app.route('/api/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({"status": "success", "message": f"{filename} deleted"})
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
