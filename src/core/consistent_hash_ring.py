import hashlib

class ConsistentHashRing:
    def __init__(self, nodes: list):
        """
        Initialize the consistent hash ring with given nodes.
        :param nodes: A list of node objects, each with a unique node_id.
        """
        self.ring = {}  # Mapping of hash value to node_id
        self.sorted_keys = []  # Sorted list of hash values
        for node in nodes:
            self.add_node(node.node_id)

    def hash_value(self, key: str) -> int:
        """
        Compute the hash of a key using MD5.
        :param key: The key to hash.
        :return: The integer hash value.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node_id: str):
        """
        Add a new node to the hash ring.
        :param node_id: The unique identifier for the node.
        """
        node_hash = self.hash_value(node_id)
        if node_hash in self.ring:
            raise ValueError(f"Node ID {node_id} already exists in the ring.")
        self.ring[node_hash] = node_id
        self.sorted_keys.append(node_hash)
        self.sorted_keys.sort()

    def remove_node(self, node_id: str):
        """
        Remove a node from the hash ring.
        :param node_id: The unique identifier for the node to remove.
        """
        node_hash = self.hash_value(node_id)
        if node_hash in self.ring:
            del self.ring[node_hash]
            self.sorted_keys.remove(node_hash)
        else:
            raise ValueError(f"Node ID {node_id} not found in the ring.")

    def get_node(self, key: str) -> str:
        """
        Find the appropriate node for a given key.
        :param key: The key for which to find the responsible node.
        :return: The node_id of the responsible node.
        """
        if not self.ring:
            raise ValueError("Hash ring is empty. No nodes available.")

        key_hash = self.hash_value(key)
        for node_hash in self.sorted_keys:
            if key_hash <= node_hash:
                return self.ring[node_hash]

        # Wraparound: If no node_hash >= key_hash, return the first node in the sorted list
        return self.ring[self.sorted_keys[0]]

    def get_node_idx(self, key: str) -> int:
        """
        Get the index of the node responsible for a given key.
        Useful for implementing replication.
        :param key: The key for which to find the responsible node index.
        :return: The index of the responsible node in the sorted list.
        """
        key_hash = self.hash_value(key)
        for i, node_hash in enumerate(self.sorted_keys):
            if key_hash <= node_hash:
                return i
        return 0  # Wraparound to the first node
