from dependencies import get_db
from fastapi import APIRouter, Depends, Form, HTTPException
from crud import port as crud_port
import schemas.schema as schema
from typing import List, Optional

router = APIRouter(
    prefix="/ports",
    tags=["ports"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id_node}/",response_model=List[schema.Port])
async def read_ports_by_node(id_node: int, skip: int = 0, limit: int = 100, db=Depends(get_db)):
    ports = crud_port.get_ports_by_node(db, id_node=id_node, skip=skip, limit=limit)
    return ports

@router.post("/", response_model=schema.Port)
async def create_port(port: schema.PortBase, db=Depends(get_db)):
    db_port = crud_port.get_port_by_name_in_node(db,name=port.name,id_node=port.id_node)
    if db_port:
        raise HTTPException(status_code=400, detail="There is already a port with that name in the node")
    return crud_port.create_port(db=db, port=port)

@router.delete("/{id}")
async def delete_port(id: str,db=Depends(get_db)):
    db_port = crud_port.get_port(db, id=id)
    if db_port is None:
        raise HTTPException(status_code=404, detail="Port not found")
    return crud_port.delete_port(db=db, id=id)