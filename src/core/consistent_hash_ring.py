import hashlib

class ConsistentHashRing:
    def __init__(self, nodes: list): 
        self.ring: dict = {}
        self.sorted_keys: list = []
        for node in nodes:
            self.add_node(node.node_id)

    def hash_value(self, key: str)-> int:
        """Compute the hash of a key using MD5."""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node_id(self, node_id: str):
        """Add a new node to the hash ring."""
        node_hash = self.hash_value(node_id)
        self.ring[node_hash] = node_id
        self.sorted_keys.append(node_hash)
        self.sorted_keys.sort()

    def get_node_idx(self, chunk_id: str)-> str:
        """Return the node hash closest to the given chunk hash."""
        chunk_hash = self.hash_value(chunk_id)
        for node_hash in self.sorted_keys:
            if chunk_hash <= node_hash:
                return node_hash
        return self.sorted_keys[0]
