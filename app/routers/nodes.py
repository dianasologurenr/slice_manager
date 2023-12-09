from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import node as crud_node
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/nodes",
    tags=["nodes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Node])
async def read_nodes(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    nodes = crud_node.get_nodes(db, skip=skip, limit=limit)
    return nodes

@router.get("/slice/{id}",response_model=List[schema.Node])
async def read_nodes(id: int,skip: int = 0, limit: int = 100, db=Depends(get_db)):
    nodes = crud_node.get_nodes_by_slice(db,slice_id=id, skip=skip, limit=limit)
    return nodes

@router.get("/{id}",response_model=schema.Node)
async def read_node(id: int, db=Depends(get_db)):
    db_node = crud_node.get_node(db, node_id=id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return db_node

@router.post("/", response_model=schema.Node)
async def create_node(node: schema.NodeBase, db=Depends(get_db)):
    db_node = crud_node.get_node_by_name_in_slice(db,name=node.name,id_slice=node.id_slice)
    if db_node:
        raise HTTPException(status_code=400, detail="There is already a node with that name in the slice")
    return crud_node.create_node(db=db, node=node)

@router.delete("/{id}")
async def delete_node(id: str,db=Depends(get_db)):
    db_node = crud_node.get_node(db, node_id=id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return crud_node.delete_node(db=db, node_id=id)