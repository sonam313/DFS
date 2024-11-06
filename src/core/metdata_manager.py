class MetadataManager:
    def __init__(self):
        self.file_metadata: dict = {}

    def add_file(self, file_id: str, chunk_size: int):
        """Add a new file and initialize its metadata."""
        if file_id not in self.file_metadata:
            self.file_metadata[file_id] = {
                'chunk_size': chunk_size,
                'chunks': {},  
                'replication_factor': 2,  
            }

    def add_chunk(self, file_id: str, chunk_id: str, node_id: str):
        """Add a chunk and its corresponding node_id to the file's metadata."""
        if file_id in self.file_metadata:
            self.file_metadata[file_id]['chunks'][chunk_id] = node_id

    def get_chunks(self, file_id: str)-> dict:
        """Get all chunk information for a specific file."""
        if file_id in self.file_metadata:
            return self.file_metadata[file_id]['chunks']
        return None

    def get_node_for_chunk(self, file_id: str, chunk_id: str)-> str:
        """Retrieve the node_id for a specific chunk."""
        if file_id in self.file_metadata and chunk_id in self.file_metadata[file_id]['chunks']:
            return self.file_metadata[file_id]['chunks'][chunk_id]
        return None

    def get_all_metadata(self):
        """Return all file metadata."""
        return self.file_metadata

    def update_replication_factor(self, file_id: str, new_replication_factor: int):
        """Update the replication factor for a specific file."""
        if file_id in self.file_metadata:
            self.file_metadata[file_id]['replication_factor'] = new_replication_factor
