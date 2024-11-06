import uuid
from api.endpoints import download_file
from core.consistent_hash_ring import ConsistentHashRing
from core.metdata_manager import MetadataManager
from core.node_manager import NodeManager


class FileManager:
    def __init__(self, metadata_manager: MetadataManager, node_manager: NodeManager, replication_factor: int = 2):
        self.metadata_manager: MetadataManager = metadata_manager
        self.node_manager: NodeManager = node_manager
        self.replication_factor: int = replication_factor
        self.consistent_hash: ConsistentHashRing = ConsistentHashRing(self.node_manager.nodes)

    def chunk_file(self, file: bytes) -> dict:
        """Split file into chunks"""
        chunk_size = 1024 * 1024 
        chunks: dict= {}
        for i in range(0, len(file.read()), chunk_size):
            chunk_id = f'chunk_{uuid.uuid4()}'
            chunks[chunk_id] = file.read(chunk_size)
        return chunks    

    def upload_file(self, file: bytes):
        """Upload a file with replication."""
        chunks = self.chunk_file(file)
        chunk_metadata = {}

        for chunk_id, chunk_data in chunks.items():
            node_store = []
            node_idx = chunk_id
            node_len = len(self.node_manager.nodes)
            while len(node_store) < self.replication_factor and node_len:
                node_idx = self.consistent_hash.get_node_idx(node_idx)
                node_id = self.consistent_hash.ring[node_idx]
                response = self.node_manager.nodes[node_id].upload_chunk(chunk_data)
                if response['status'] == 'success':
                    node_store.append(node_id)
                node_idx +=1
                node_len -=1

            chunk_metadata[chunk_id] = node_store  

        self.metadata_manager.store_file_metadata(file.filename, chunk_metadata)
        return {'status': 'success', 'message': 'File uploaded successfully'}

    def download_file(self, filename: str)-> dict:
        """Download a file by retrieving chunks from nodes."""
        file_metadata = self.metadata_manager.download_file(filename)

        if not file_metadata:
            return {'status': 'error', 'message': 'File not found'}

        file_data = b''

        for chunk_id, node_ids in file_metadata.items():
            chunk_retrieved = False
            for node_id in node_ids:
                node = self.node_manager.get_node_by_id(node_id)
                chunk_data = node.download_chunk(chunk_id)

                if chunk_data['status'] == 'success':
                    file_data += chunk_data['data']
                    chunk_retrieved = True
                    break 

            if not chunk_retrieved:
                return {'status': 'error', 'message': f'Failed to retrieve chunk {chunk_id}'}

        return {'status': 'success', 'data': file_data}

