import threading
import logging
import signal
import sys
from client.client import ClientServer
from master_node import MasterServer

MASTER_IP = '127.0.0.1'
MASTER_PORT = 5010

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Graceful shutdown
def shutdown(signal_received, frame):
    logging.info("Shutdown signal received. Terminating servers...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    try:
        logging.info("Initializing Master and Client servers...")

        master_server = MasterServer(MASTER_IP, MASTER_PORT)
        client_server = ClientServer(MASTER_IP, MASTER_PORT)

        master_thread = threading.Thread(target=master_server.start_master_server)
        client_thread = threading.Thread(target=client_server.start_client_server)

        # Set threads as daemons
        master_thread.daemon = True
        client_thread.daemon = True

        # Start the threads
        master_thread.start()
        client_thread.start()

        logging.info(f"MasterServer running on {MASTER_IP}:{MASTER_PORT}")
        logging.info(f"ClientServer connected to MasterServer on {MASTER_IP}:{MASTER_PORT}")

        # Keep the main thread alive
        master_thread.join()
        client_thread.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
