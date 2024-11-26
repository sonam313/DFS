from core.node_base import Node


class NodeManager:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: Node):
        """
        Add a new node to the system.
        :param node: Node object to be added.
        """
        if node.node_id in self.nodes:
            raise ValueError(f"Node with ID {node.node_id} already exists.")
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str):
        """
        Remove a node from the system.
        :param node_id: ID of the node to be removed.
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
        else:
            raise ValueError(f"Node with ID {node_id} does not exist.")

    def get_available_node(self) -> Node:
        """
        Get the first node that has available storage space.
        :return: A Node object or None if no node is available.
        """
        for node in self.nodes.values():
            if node.is_available():
                return node
        return None

    def get_node_by_id(self, node_id: str) -> Node:
        """
        Find a node by its ID.
        :param node_id: ID of the node to find.
        :return: The Node object if found, or None.
        """
        return self.nodes.get(node_id)

    def list_nodes(self) -> list:
        """
        List all nodes managed by the system.
        :return: A list of Node objects.
        """
        return list(self.nodes.values())

    def get_node_status(self) -> dict:
        """
        Retrieve the status of all nodes.
        :return: A dictionary with node IDs as keys and their statuses as values.
        """
        return {node_id: node.get_status() for node_id, node in self.nodes.items()}
