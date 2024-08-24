import socket
import os
import threading
import json

import os
NODE_ID = 'node1'           # Unique ID for the node
NODE_IP = '127.0.0.1'       # Node IP address
NODE_PORT = 5007            # Node port number
STORAGE_DIR = 'C:\\Users\\Sonam\\Desktop\\node_storage'  # Directory to store chunks

# Ensure the storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)


def register_with_master():
    """Register the node with the master node."""
    master_ip = '127.0.0.1'
    master_port = 5000
    node_info = {'node_id': NODE_ID, 'chunks': os.listdir(STORAGE_DIR)}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((master_ip, master_port))
        s.send(json.dumps(node_info).encode('utf-8'))

def handle_chunk_request(conn):
    """Handle incoming requests to store or retrieve chunks."""
    request = conn.recv(1024).decode('utf-8')
    request_data = json.loads(request)
    action = request_data['action']

    if action == 'store_chunk':
        chunk_name = request_data['chunk_name']
        chunk_data = conn.recv(1024 * 1024)  # Assuming chunk size is <= 1 MB
        with open(os.path.join(STORAGE_DIR, chunk_name), 'wb') as chunk_file:
            chunk_file.write(chunk_data)
        response = {'status': 'success'}

    elif action == 'get_chunk':
        chunk_name = request_data['chunk_name']
        chunk_path = os.path.join(STORAGE_DIR, chunk_name)
        if os.path.exists(chunk_path):
            with open(chunk_path, 'rb') as chunk_file:
                chunk_data = chunk_file.read()
            response = {'status': 'success', 'chunk_data': chunk_data}
        else:
            response = {'status': 'error', 'message': 'Chunk not found'}

    conn.send(json.dumps(response).encode('utf-8'))
    conn.close()

def node_server():
    """Main loop to listen for chunk storage/retrieval requests."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((NODE_IP, NODE_PORT))
    server_socket.listen(5)
    print(f"Node {NODE_ID} listening on {NODE_IP}:{NODE_PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_chunk_request, args=(conn,)).start()

if __name__ == "__main__":
    register_with_master()
    node_server()
