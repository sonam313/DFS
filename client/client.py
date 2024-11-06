import socket
import threading

from src.master_node import MasterServer

class ClientServer():

    def __init__(self,master_ip, master_port):
        self.master_ip = master_ip
        self.master_port = master_port

    def client_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.master_ip, self.master_port) + 1))
        client_socket.listen(5)
        print(f"Client server listening on {self.master_ip}:{self.master_port + 1}")
        
        master_server = MasterServer(self.master_ip, self.master_port) 
        while True:
            conn, addr = client_socket.accept()
            threading.Thread(target=master_server.handle_client_request, args=(conn, )).start()

    
 