class MetadataManager:
    def __init__(self):
        self.file_metadata = {}

    def add_file(self, file_id: str, chunk_size: int, replication_factor: int = 2):
        """
        Add a new file and initialize its metadata.
        :param file_id: Unique identifier for the file.
        :param chunk_size: Size of each file chunk.
        :param replication_factor: Default replication factor for the file.
        """
        if file_id in self.file_metadata:
            raise ValueError(f"File with ID {file_id} already exists.")
        self.file_metadata[file_id] = {
            'chunk_size': chunk_size,
            'chunks': {},  
            'replication_factor': replication_factor,
        }

    def add_chunk(self, file_id: str, chunk_id: str, node_ids: list):
        """
        Add a chunk and its corresponding node_ids to the file's metadata.
        :param file_id: ID of the file to which the chunk belongs.
        :param chunk_id: Unique identifier for the chunk.
        :param node_ids: List of node IDs where the chunk is stored.
        """
        if file_id not in self.file_metadata:
            raise ValueError(f"File with ID {file_id} does not exist.")
        if chunk_id in self.file_metadata[file_id]['chunks']:
            raise ValueError(f"Chunk {chunk_id} already exists in file {file_id}.")
        self.file_metadata[file_id]['chunks'][chunk_id] = node_ids

    def get_chunks(self, file_id: str) -> dict:
        """
        Get all chunk information for a specific file.
        :param file_id: ID of the file.
        :return: Dictionary of chunks and their associated nodes.
        """
        if file_id not in self.file_metadata:
            return None
        return self.file_metadata[file_id]['chunks']

    def get_nodes_for_chunk(self, file_id: str, chunk_id: str) -> list:
        """
        Retrieve the node IDs for a specific chunk.
        :param file_id: ID of the file.
        :param chunk_id: ID of the chunk.
        :return: List of node IDs storing the chunk.
        """
        if file_id in self.file_metadata and chunk_id in self.file_metadata[file_id]['chunks']:
            return self.file_metadata[file_id]['chunks'][chunk_id]
        return None

    def get_file_metadata(self, file_id: str) -> dict:
        """
        Retrieve metadata for a specific file.
        :param file_id: ID of the file.
        :return: Dictionary containing the file's metadata.
        """
        return self.file_metadata.get(file_id, None)

    def get_all_metadata(self) -> dict:
        """
        Return all file metadata.
        :return: Dictionary of all files and their metadata.
        """
        return self.file_metadata

    def update_replication_factor(self, file_id: str, new_replication_factor: int):
        """
        Update the replication factor for a specific file.
        :param file_id: ID of the file.
        :param new_replication_factor: New replication factor to be set.
        """
        if file_id not in self.file_metadata:
            raise ValueError(f"File with ID {file_id} does not exist.")
        self.file_metadata[file_id]['replication_factor'] = new_replication_factor

    def remove_file(self, file_id: str):
        """
        Remove a file and its metadata from the system.
        :param file_id: ID of the file to be removed.
        """
        if file_id in self.file_metadata:
            del self.file_metadata[file_id]
        else:
            raise ValueError(f"File with ID {file_id} does not exist.")
