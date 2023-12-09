from dependencies import get_db
from fastapi import APIRouter, Depends, Form, HTTPException
from crud import node as crud_node
import schemas.schema as schema
from typing import List, Optional

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
    db_node = crud_node.get_node(db, id=id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return db_node

@router.post("/", response_model=schema.Node)
async def create_node(node: schema.NodeBase, db=Depends(get_db)):
    db_node = crud_node.get_node_by_name_in_slice(db,name=node.name,id_slice=node.id_slice)
    if db_node:
        raise HTTPException(status_code=400, detail="There is already a node with that name in the slice")
    return crud_node.create_node(db=db, node=node)

@router.patch("/{id}", response_model=schema.Node)
async def update_node(id: int, 
                 id_image: Optional[str] = Form(None),
                 id_server: Optional[str] = Form(None),
                 id_security: Optional[str] = Form(None),
                 id_flavor: Optional[str] = Form(None),
                 db=Depends(get_db)):
    db_node = crud_node.get_node(db=db, id=id)
    
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    update_node = schema.NodeUpdate()

    if id_image:
        update_node.id_image = id_image
    if id_server:
        update_node.id_server = id_server
    if id_security:
        update_node.id_security = id_security
    if id_flavor:
        update_node.id_flavor = id_flavor
    
    return crud_node.update_node(db=db,id=id,node=update_node)



@router.delete("/{id}")
async def delete_node(id: str,db=Depends(get_db)):
    db_node = crud_node.get_node(db, id=id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return crud_node.delete_node(db=db, node_id=id)