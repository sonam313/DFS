# client/client.py
from flask import Flask, request, jsonify

app = Flask(__name__)

class ClientServer:
    def __init__(self, master_ip, master_port):
        self.master_ip = master_ip
        self.master_port = master_port

    def start_client_server(self):
        """Start the client simulation server."""
        app.run(host='127.0.0.1', port=5001)

    @app.route('/upload_chunk', methods=['POST'])
    def upload_chunk():
        chunk_data = request.files['file']
        # Logic to handle the uploaded chunk
        return jsonify({"status": "Chunk uploaded"}), 200
