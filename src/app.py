"""
Exercise 01 — Node Registry API

Implement a FastAPI application with the following endpoints:

GET    /health          → health check with DB status
POST   /api/nodes       → register a new node
GET    /api/nodes       → list all nodes
GET    /api/nodes/{name} → get a node by name
PUT    /api/nodes/{name} → update a node
DELETE /api/nodes/{name} → soft-delete a node (set status=inactive)

See README.md for full specification.
"""

# TODO: Implement your FastAPI app here
from fastapi import FastAPI, HTTPException, status, Depends
from schemas import NodeCreate, NodeResponse, NodeUpdate, HealthResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Nodes
from sqlalchemy import exc, delete, update, select, func, insert
import uvicorn



app = FastAPI()
init_db()

@app.get("/health",
         response_model=HealthResponse)
def health_check(db:Session =Depends(get_db)):
    try:
        stm = select(func.count(Nodes.id)).select_from(Nodes).where(Nodes.status == "active")
    
        nodes_count = db.execute(stm).scalar()
        response = HealthResponse(status="ok", db="connected",nodes_count=nodes_count)
    except:
        response = HealthResponse(status="ok", db="disconnected", nodes_count=0)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())


@app.post("/api/nodes", 
          response_model=NodeResponse,
          status_code= status.HTTP_201_CREATED)
def register_node(query: NodeCreate, db:Session =Depends(get_db)):
    """
    Register a node
    """
    nuevo_nodo = Nodes(
        name= query.name,
        host= query.host,
        port= query.port
    )
    
    try:
        db.add(nuevo_nodo)
        db.commit()
        db.refresh(nuevo_nodo)
    except  exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Node exist in DB")

    return nuevo_nodo


@app.get("/api/nodes" ,status_code= status.HTTP_200_OK)
def list_nodes(db:Session = Depends(get_db)):
    all_nodes = db.query(Nodes).all()
    nodesResponse = []
    for nodo in all_nodes:
        nodesResponse.append(nodo)
    return nodesResponse

@app.get("/api/nodes/{name}", response_model= NodeResponse,status_code= status.HTTP_200_OK )
def get_by_name(name: str, db:Session =Depends(get_db)):
    smt = select(Nodes).select_from(Nodes).where(Nodes.name == name)
    node = db.execute(smt).scalar()
    if (node is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return node

@app.put("/api/nodes/{name}", response_model=NodeResponse, status_code=status.HTTP_200_OK)
def update_node(name: str, updated: NodeUpdate, db:Session =Depends(get_db)):

    update_data = updated.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No information provided for update")
    
    stm = select(Nodes).where(Nodes.name == name)
    node = db.execute(stm).scalar_one_or_none()

    if (node is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    


    for key, value in update_data.items():
        setattr(node, key, value)

    try:
        db.commit()
        db.refresh(node)
        return node 
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Update violates integrity constraints")
    
@app.delete("/api/nodes/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(name: str, db:Session =Depends(get_db)):
    """
    Delete node
    """
    smt = select(Nodes).where(Nodes.name == name)
    node = db.scalar(smt)

    if (node is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    node.status = "inactive"
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")

