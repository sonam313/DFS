from datetime import datetime
from core.node_base import Node
from core.metadata_manager import MetadataManager
from core.file_manager import FileManager
from core.node_manager import NodeManager
from datamodel import Config

class MasterServer:
    def __init__(self, master_ip: str, master_port: int):
        self.master_ip = master_ip
        self.master_port = master_port
        self.node_manager = NodeManager()
        self.metadata_manager = MetadataManager()
        self.file_manager = FileManager(self.metadata_manager, self.node_manager)

    def start_master_server(self):
        print(f"Master server started at {self.master_ip}:{self.master_port}")
        # Add server logic to handle incoming requests here
        # For example, accepting client connections and interacting with NodeManager, MetadataManager, FileManager

    def add_node(self, node: Node):
        self.node_manager.add_node(node)
        print(f"Node {node.node_id} added.")

    def get_node_info(self):
        return self.node_manager.get_all_nodes()

    def upload_file(self, file_id: str, chunk_data: bytes):
        # Assuming file and chunk data is processed
        node = self.node_manager.get_available_node()
        if node:
            response = node.upload_chunk(chunk_data)
            return response
        else:
            return {"status": "error", "message": "No available nodes"}

    def download_file(self, file_id: str, chunk_id: str):
        node_id = self.metadata_manager.get_node_for_chunk(file_id, chunk_id)
        node = self.node_manager.get_node_by_id(node_id)
        if node:
            return node.download_chunk(chunk_id)
        return {"status": "error", "message": "Chunk not found"}

