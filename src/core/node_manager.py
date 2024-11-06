from core.node_base import Node

class NodeManager:
    def __init__(self):
        self.nodes = []  

    def add_node(self, node: Node):
        """Add a new node to the system."""
        self.nodes.append(node)

    def get_available_node(self)-> Node:
        """Get a node that has storage space."""
        for node in self.nodes:
            if node.is_available():
                return node
        return None

    def get_node_by_id(self, node_id)-> Node:
        """Find a node by its ID."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
   