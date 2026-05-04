"""
SQLAlchemy model for the nodes table.

Table: nodes
- id: SERIAL PRIMARY KEY
- name: VARCHAR UNIQUE NOT NULL
- host: VARCHAR NOT NULL
- port: INTEGER NOT NULL
- status: VARCHAR DEFAULT 'active'
- created_at: TIMESTAMP DEFAULT NOW()
- updated_at: TIMESTAMP DEFAULT NOW()
"""

# TODO: Implement your SQLAlchemy model here
from sqlalchemy import String, VARCHAR, Integer, TIMESTAMP, func

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base

class Nodes(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(Integer,  
                                    primary_key=True, 
                                    autoincrement=True)
    
    name: Mapped[str] = mapped_column(String,
                                      unique=True, 
                                      nullable=False)

    host: Mapped[str] = mapped_column(String,
                                      nullable=False)

    port: Mapped[int] = mapped_column(Integer,
                                      nullable=False)
    
    status: Mapped[str] = mapped_column(VARCHAR,
                                         default="active", 
                                         server_default="active")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                  default=func.now(), 
                                                 server_default=func.now())
    
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, 
                                                 default=func.now(), 
                                                 server_default=func.now()
                                                 , onupdate=func.now())
                                