from flask import Flask, request, jsonify
import logging
import json
from src.core.file_manager import FileManager
from src.core.node_manager import NodeManager
from src.datamodel import Config

app = Flask(__name__)

config = Config(master_ip='127.0.0.1', master_port=5000)
node_manager = NodeManager()
file_manager = FileManager(node_manager.nodes)

@app.route('/register_node', methods=['POST'])
def register_node():
    try:
        node_info = request.json
        node_manager.handle_node_registration(node_info)  
        return jsonify({"status": "success", "message": "Node registered successfully"})
    except Exception as e:
        logging.error(f"Error in node registration: {e}")
        return jsonify({"status": "error", "message": "Failed to register node"}), 500

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"})

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"})

        response = file_manager.file_upload(file)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in file upload: {e}")
        return jsonify({"status": "error", "message": "Failed to upload file"}), 500

@app.route('/download_chunk/<chunk_id>', methods=['GET'])
def download_chunk(chunk_id):
    try:
        # File download logic
        file_chunk = file_manager.file_download(chunk_id)
        if file_chunk:
            return jsonify({"status": "success", "file_data": file_chunk})
        else:
            return jsonify({"status": "error", "message": "File chunk not found"}), 404
    except Exception as e:
        logging.error(f"Error in file download: {e}")
        return jsonify({"status": "error", "message": "Failed to download file"}), 500

if __name__ == "__main__":
    app.run(host=config.master_ip, port=config.master_port, debug=True)
