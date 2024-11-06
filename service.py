import threading
from master.master import MasterServer
from client.client import ClientServer

MASTER_IP = '127.0.0.1'
MASTER_PORT = 5010

if __name__ == "__main__":
    master_server = MasterServer(MASTER_IP, MASTER_PORT)
    client_server = ClientServer(MASTER_IP, MASTER_PORT)
    
    threading.Thread(target = master_server.start_master_server).start()
    threading.Thread(target = client_server.start_client_server).start()
