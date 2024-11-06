from pydantic import BaseModel
import datetime
from enum import Enum

class Config(BaseModel):
    master_ip: str
    master_port: str
    replication_factor: int = 2
    nodes: dict = {}
    files_metadata: dict = {}
    block_size: str = "1MB"
    cpu_load: str  = ""
    memory_usage: str  = "2GB"

class NodeStatusEnum(Enum):
    Online = "Online"
    Offline = "Offline"

class NodeTypeEnum(Enum):
    Storage = "Storage"
    Compute = "Compute"    

class Node_Info(BaseModel): 
    node_id: str 
    ip_address: str   
    port: int                    
    total_storage: str         
    available_storage: str  
    status: NodeStatusEnum              
    node_type: NodeTypeEnum          
    last_updated: datetime