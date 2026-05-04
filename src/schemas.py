"""
Pydantic schemas for request/response validation.

NodeCreate: for POST body (name, host, port — all required)
NodeUpdate: for PUT body (host, port — optional)
NodeResponse: for API responses (includes id, status, timestamps)
"""

# TODO: Implement your Pydantic schemas here

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class NodeCreate(BaseModel):
    """
    params:
        - name 
        - host 
        - port
    """
    name:str = Field(..., min_length=1)
    host:str = Field(..., min_length=1)
    port:int = Field(..., gt=0, lt=65536)

class NodeUpdate(BaseModel):
    """
    params:
        - host 
        - port| None
    """
    host: Optional[str] = Field(default=None, min_length=1)
    port: int | None = Field(default=None, gt=1, lt=65536)


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
    updated_at: datetime

    class Config:
        from_attributes=True

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