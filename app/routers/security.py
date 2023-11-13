from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import security as crud_security
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/security",
    tags=["security"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.SecurityGroup])
async def read_security_groups(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    security_groups = crud_security.get_security_groups(db, skip=skip, limit=limit)
    return security_groups


@router.post("/", response_model=schema.SecurityGroup)
async def create_security_group(security_group: schema.SecurityGroupBase, db=Depends(get_db)):
    db_security_group = crud_security.get_security_group_by_name(db,name=security_group.name)
    if db_security_group:
        raise HTTPException(status_code=40, detail="Security group already registered")
    return crud_security.create_security_groups(db=db, security_group=security_group)


@router.delete("/{id}")
async def delete_security_group(id: int,db=Depends(get_db)):
    db_security_group = crud_security.get_security_group_by_id(db,id=id)
    if db_security_group is None:
        raise HTTPException(status_code=404, detail="Security group not found")
    return crud_security.delete_security_groups(db=db, security_group_id=id)