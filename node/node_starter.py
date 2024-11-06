from dataclasses import dataclass
from src.core.node_base import Node

@dataclass
class Node_Info():
    node_id :str 
    storage_dir :str 
    node_ip :str
    node_port :int


AVAILABLE_NODES = [Node_Info("node1",'C:\\Users\\Sonam\\Desktop\\node_storage\\node_1','127.0.0.1',5009),
                   Node_Info("node1",'C:\\Users\\Sonam\\Desktop\\node_storage\\node_2','127.0.0.1',5008), ]

def main():
    for n in AVAILABLE_NODES:
        node = Node(node_id = n.node_id, 
                    storage_dir = n.storage_dir, 
                    node_ip = n.node_ip,
                    node_port = n.node_port
            )
        
        node.register_with_master()
        print(f"succesfully registered node: {n.node_id}")

        node.node_server()
        
if __name__ == "__main__":
    main()        