import requests

class Node:
    def __init__(self, node_id: str, ip, port: str):
        self.node_id = node_id
        self.ip = ip
        self.port = port

    def upload_chunk(self, chunk_data: bytes):
        """Send a chunk to the node for storage."""
        url = f'http://{self.ip}:{self.port}/upload'
        files = {'file': chunk_data}

        try:
            response = requests.post(url, files = files)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

    def download_chunk(self, chunk_id: str)-> dict:
        """Retrieve a chunk from the node."""
        url = f'http://{self.ip}:{self.port}/download/{chunk_id}'

        try:
            response = requests.get(url)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

    def is_available(self):
        """Check if the node has available storage."""
        return True
