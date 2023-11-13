from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import inbound as crud_inbound
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/inbound",
    tags=["inbound"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.inBound])
async def read_inbounds(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    inbound = crud_inbound.get_inbound(db, skip=skip, limit=limit)
    return inbound

@router.get("/{id}",response_model=List[schema.inBound])
async def read_inboundsPerSecurityGroup(id: int , skip: int = 0, limit: int = 100, db=Depends(get_db)):
    inbound = crud_inbound.get_inbound_byIdSecurity(db, inbound_idSecurity=id , skip=skip, limit=limit)
    return inbound

@router.post("/", response_model=schema.inBound)
async def create_inbound(inbound: schema.inBoundBase, db=Depends(get_db)):
    return crud_inbound.create_inbound(db=db, inbound=inbound)

@router.delete("/{id}")
async def delete_inbound(id: str,db=Depends(get_db)):
    db_inbound = crud_inbound.get_inbound_byID(db, inbound_id=id)
    if db_inbound is None:
        raise HTTPException(status_code=404, detail="Inbound not found")
    return crud_inbound.delete_inbound(db=db, inbound_id=id)