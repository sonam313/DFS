import uuid
from core.consistent_hash_ring import ConsistentHashRing
from core.metadata_manager import MetadataManager
from core.node_manager import NodeManager


class FileManager:
    def __init__(self, metadata_manager: MetadataManager, node_manager: NodeManager, replication_factor: int = 2):
        self.metadata_manager: MetadataManager = metadata_manager
        self.node_manager: NodeManager = node_manager
        self.replication_factor: int = replication_factor
        self.consistent_hash: ConsistentHashRing = ConsistentHashRing(self.node_manager.nodes)

    def chunk_file(self, file: bytes) -> dict:
        """Split file into chunks."""
        chunk_size = 1024 * 1024  # 1 MB per chunk
        file_data = file.read()
        chunks = {}
        for i in range(0, len(file_data), chunk_size):
            chunk_id = f'chunk_{uuid.uuid4()}'
            chunks[chunk_id] = file_data[i:i + chunk_size]
        return chunks

    def upload_file(self, file) -> dict:
        """Upload a file with replication."""
        chunks = self.chunk_file(file)
        chunk_metadata = {}
        nodes = self.node_manager.nodes

        if not nodes:
            return {'status': 'error', 'message': 'No available nodes for file upload'}

        for chunk_id, chunk_data in chunks.items():
            node_store = []
            attempts = 0

            while len(node_store) < self.replication_factor and attempts < len(nodes):
                # Get the next node for storing the chunk
                node_id = self.consistent_hash.get_node(chunk_id)
                response = nodes[node_id].upload_chunk(chunk_data)

                if response.get('status') == 'success':
                    node_store.append(node_id)

                # Avoid infinite loops in case of node failures
                attempts += 1

            if len(node_store) < self.replication_factor:
                return {'status': 'error', 'message': f'Failed to upload chunk {chunk_id} to enough nodes'}

            chunk_metadata[chunk_id] = node_store

        # Store metadata for the file
        unique_filename = f"{file.filename}_{uuid.uuid4()}"
        self.metadata_manager.store_file_metadata(unique_filename, chunk_metadata)
        return {'status': 'success', 'message': 'File uploaded successfully', 'filename': unique_filename}

    def download_file(self, filename: str) -> dict:
        """Download a file by retrieving chunks from nodes."""
        file_metadata = self.metadata_manager.get_file_metadata(filename)

        if not file_metadata:
            return {'status': 'error', 'message': 'File not found'}

        file_data = b''

        for chunk_id, node_ids in file_metadata.items():
            chunk_retrieved = False

            for node_id in node_ids:
                node = self.node_manager.get_node_by_id(node_id)

                if not node:
                    continue

                response = node.download_chunk(chunk_id)

                if response.get('status') == 'success' and 'data' in response:
                    file_data += response['data']
                    chunk_retrieved = True
                    break

            if not chunk_retrieved:
                return {'status': 'error', 'message': f'Failed to retrieve chunk {chunk_id}'}

        return {'status': 'success', 'data': file_data}
