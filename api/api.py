from flask import Flask, request, jsonify, send_file
import os
import requests

app = Flask(__name__)

# Configuration
MASTER_NODE_URL = 'http://localhost:5000'
UPLOAD_FOLDER = '/path/to/upload_folder'  # Folder to temporarily store uploaded files

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Send file to the master node to handle chunking and distribution
    files = {'file': open(file_path, 'rb')}
    response = requests.post(f'{MASTER_NODE_URL}/distribute', files=files)

    # Clean up the temporary file
    os.remove(file_path)

    if response.status_code == 200:
        return jsonify({'message': 'File successfully uploaded and distributed'}), 200
    else:
        return jsonify({'error': 'Error distributing file'}), 500

# Endpoint to download a file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    response = requests.get(f'{MASTER_NODE_URL}/reassemble', params={'filename': filename})
    if response.status_code == 200:
        # Save the reassembled file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Error retrieving file'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5001, debug=True)
