import socket
import threading
import json
import os

MASTER_IP = '127.0.0.1'
MASTER_PORT = 5000
CHUNK_SIZE = 1024 * 1024  # 1 MB chunks
REPLICATION_FACTOR = 2    # Number of nodes to replicate each chunk

nodes = {}
file_chunks = {}

def split_file(file_path):
    """Split the file into chunks of fixed size."""
    chunks = []
    with open(file_path, 'rb') as f:
        chunk_num = 0
        while chunk := f.read(CHUNK_SIZE):
            chunk_filename = f"{os.path.basename(file_path)}_chunk_{chunk_num}"
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunks.append(chunk_filename)
            chunk_num += 1
    return chunks

def handle_node_registration(conn, addr):
    """Handle the registration of nodes and their available storage."""
    data = conn.recv(1024).decode('utf-8')
    node_info = json.loads(data)
    node_id = node_info['node_id']
    nodes[node_id] = addr
    conn.close()

def distribute_chunks(chunks):
    """Distribute file chunks to nodes with replication."""
    chunk_locations = {}
    node_ids = list(nodes.keys())
    for i, chunk in enumerate(chunks):
        for j in range(REPLICATION_FACTOR):
            node_id = node_ids[(i + j) % len(node_ids)]
            chunk_locations[chunk] = chunk_locations.get(chunk, []) + [node_id]
    return chunk_locations

def master_server():
    """Main loop for the master node to handle node registrations."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((MASTER_IP, MASTER_PORT))
    server_socket.listen(5)
    print(f"Master server listening on {MASTER_IP}:{MASTER_PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_node_registration, args=(conn, addr)).start()

def handle_client_request(client_socket):
    """Handle client requests for uploading or downloading files."""
    request = client_socket.recv(1024).decode('utf-8')
    request_data = json.loads(request)
    action = request_data['action']

    if action == 'upload':
        file_path = request_data['file_path']
        chunks = split_file(file_path)
        chunk_locations = distribute_chunks(chunks)
        file_chunks[os.path.basename(file_path)] = chunk_locations
        response = {'status': 'success', 'chunk_locations': chunk_locations}

    elif action == 'download':
        file_name = request_data['file_name']
        if file_name in file_chunks:
            response = {'status': 'success', 'chunk_locations': file_chunks[file_name]}
        else:
            response = {'status': 'error', 'message': 'File not found'}

    client_socket.send(json.dumps(response).encode('utf-8'))
    client_socket.close()

def client_server():
    """Secondary server loop for handling client requests."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((MASTER_IP, MASTER_PORT + 1))
    client_socket.listen(5)
    print(f"Client server listening on {MASTER_IP}:{MASTER_PORT + 1}")

    while True:
        conn, addr = client_socket.accept()
        threading.Thread(target=handle_client_request, args=(conn, addr)).start()

if __name__ == "__main__":
    threading.Thread(target=master_server).start()
    threading.Thread(target=client_server).start()
