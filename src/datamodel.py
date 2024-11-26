from pydantic import BaseModel, Field
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

    class Config:
        schema_extra = {
            "example": {
                "master_ip": "127.0.0.1",
                "master_port": 5010,
                "replication_factor": 3,
                "nodes": {},
                "files_metadata": {},
                "block_size": "4MB",
                "cpu_load": "20%",
                "memory_usage": "8GB",
            }
        }

class NodeStatusEnum(str, Enum):
    Online = "Online"
    Offline = "Offline"

class NodeTypeEnum(str, Enum):
    Storage = "Storage"
    Compute = "Compute"

class Node_Info(BaseModel):
    node_id: str
    ip_address: str
    port: int
    total_storage:  str 
    available_storage: str
    status: NodeStatusEnum = NodeStatusEnum.Offline
    node_type: NodeTypeEnum = NodeTypeEnum.Storage
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def update_status(self, new_status: NodeStatusEnum):
        """Update the status of the node."""
        self.status = new_status
        self.last_updated = datetime.datetime.now()

    def update_available_storage(self, used_storage: int):
        """Reduce available storage and update last modified time."""
        available = int(self.available_storage[:-2]) - used_storage
        self.available_storage = f"{max(available, 0)}GB"
        self.last_updated = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "node_id": "node_001",
                "ip_address": "192.168.1.10",
                "port": 8080,
                "total_storage": "500GB",
                "available_storage": "450GB",
                "status": "Online",
                "node_type": "Storage",
                "last_updated": "2024-11-25T12:00:00",
            }
        }
