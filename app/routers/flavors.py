from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import flavor as crud_flavor
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/flavors",
    tags=["flavors"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Flavor])
async def read_flavors(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    flavors= crud_flavor.get_flavors(db, skip=skip, limit=limit)
    return flavors

@router.get("/{id}",response_model=schema.Flavor)
async def read_flavor(id: int, db=Depends(get_db)):
    db_flavor = crud_flavor.get_flavor(db, flavor_id=id)
    if db_flavor is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_flavor

"""@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db=Depends(get_db)):
    db_user = crud_user.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=40, detail="Email already registered")
    temp = crud_user.get_user_by_username(db,username=user.username)
    if temp:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)"""

@router.delete("/{id}")
async def delete_user(id: str,db=Depends(get_db)):
    db_flavor = crud_flavor.get_flavor(db, flavor_id=id)
    if db_flavor is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_flavor.delete_flavor(db=db, flavor_id=id)