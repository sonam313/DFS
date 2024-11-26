import requests

class Node:
    def __init__(self, node_id: str, ip: str, port: str):
        """
        Initialize a node with its unique ID, IP address, and port.
        :param node_id: Unique identifier for the node.
        :param ip: IP address of the node.
        :param port: Port number for the node's API.
        """
        self.node_id = node_id
        self.ip = ip
        self.port = port

    def upload_chunk(self, chunk_data: bytes, chunk_id: str) -> dict:
        """
        Send a chunk to the node for storage.
        :param chunk_data: The binary data of the chunk.
        :param chunk_id: Unique identifier for the chunk.
        :return: Response from the node.
        """
        url = f'http://{self.ip}:{self.port}/upload'
        files = {'file': chunk_data}
        data = {'chunk_id': chunk_id}

        try:
            response = requests.post(url, files=files, data=data, timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': f'Failed to upload chunk {chunk_id}: {str(e)}'}

    def download_chunk(self, chunk_id: str) -> dict:
        """
        Retrieve a chunk from the node.
        :param chunk_id: Unique identifier of the chunk to download.
        :return: Response containing the chunk data or an error message.
        """
        url = f'http://{self.ip}:{self.port}/download/{chunk_id}'

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return {'status': 'success', 'data': response.content}
            else:
                return {'status': 'error', 'message': f'Error {response.status_code}: {response.text}'}
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': f'Failed to download chunk {chunk_id}: {str(e)}'}

    def is_available(self) -> bool:
        """
        Check if the node is available for new storage.
        This should ideally ping a health or status endpoint.
        :return: True if the node is available, False otherwise.
        """
        url = f'http://{self.ip}:{self.port}/health'

        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            return False
