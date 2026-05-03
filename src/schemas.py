"""
Pydantic schemas for request/response validation.

NodeCreate: for POST body (name, host, port — all required)
NodeUpdate: for PUT body (host, port — optional)
NodeResponse: for API responses (includes id, status, timestamps)
"""

# TODO: Implement your Pydantic schemas here

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NodeCreate(BaseModel):
    """
    params:
        - name 
        - host 
        - port
    """
    name:str
    host:str
    port:int

class NodeUpdate(BaseModel):
    """
    params:
        - host 
        - port| None
    """
    host:str
    port: Optional[str]

class NodeResponse(BaseModel):
    """
    params:
        - id 
        - name 
        - host
        - port
        - status
        - created_at
        - update_at
    """
    id : int
    name : str
    host: str
    port: int
    status: str
    created_at: datetime
    update_at: datetime

class HealthResponse(BaseModel):
    """
    params:
        - status
        - db
        - nodes_count
    """
    status:str
    db: str
    nodes_count: int