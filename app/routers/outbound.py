from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import outbound as crud_outbound
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/outbound",
    tags=["outbound"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.outBound])
async def read_outbounds(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    outbound = crud_outbound.get_outbound(db, skip=skip, limit=limit)
    return outbound

@router.get("/{id}",response_model=List[schema.inBound])
async def read_outboundsPerSecurityGroup(id: int , skip: int = 0, limit: int = 100, db=Depends(get_db)):
    inbound = crud_outbound.get_outbound_byIdSecurity(db, outbound_idSecurity=id , skip=skip, limit=limit)
    return inbound


@router.post("/", response_model=schema.outBound)
async def create_outbound(outbound: schema.outBoundBase, db=Depends(get_db)):
    return crud_outbound.create_outbound(db=db, outbound=outbound)

@router.delete("/{id}")
async def delete_inbound(id: str,db=Depends(get_db)):
    db_outbound = crud_outbound.get_outbound_byID(db, outbound_id=id)
    if db_outbound is None:
        raise HTTPException(status_code=404, detail="Outbound not found")
    return crud_outbound.delete_outbound(db=db, outbound_id=id)