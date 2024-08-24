import os
NODE_ID = 'node1'           # Unique ID for the node
NODE_IP = '127.0.0.1'       # Node IP address
NODE_PORT = 5001            # Node port number
STORAGE_DIR = 'C:\\Users\\Sonam\\Desktop\\node_storage'  # Directory to store chunks

# Ensure the storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)
