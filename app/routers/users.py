from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import user as crud_user
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.User])
async def read_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{id}",response_model=schema.User)
async def read_user(id: int, db=Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db=Depends(get_db)):
    db_user = crud_user.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=40, detail="Email already registered")
    temp = crud_user.get_user_by_username(db,username=user.username)
    if temp:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)

@router.delete("/{id}")
async def delete_user(id: str,db=Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db=db, user_id=id)