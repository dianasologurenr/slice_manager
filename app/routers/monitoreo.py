from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import server as crud_server
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/monitoreo",
    tags=["monitoreo"],
    responses={404: {"description": "Not found"}},
)

@router.get("/servers",response_model=List[schema.Server])
async def read_server(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    servers = crud_server.get_servers(db, skip=skip, limit=limit)
    return servers

@router.get("/servers/{id}",response_model=schema.Server)
async def read_server(id: int, db=Depends(get_db)):
    db_server = crud_server.get_server(db, id=id)
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server

# @router.post("/", response_model=schema.User)
# async def create_user(user: schema.UserCreate, db=Depends(get_db)):
#     db_user = crud_server.get_user_by_email(db,email=user.email)
#     if db_user:
#         raise HTTPException(status_code=40, detail="Email already registered")
#     temp = crud_server.get_user_by_username(db,username=user.username)
#     if temp:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return crud_server.create_user(db=db, user=user)

# @router.delete("/{id}")
# async def delete_user(id: str,db=Depends(get_db)):
#     db_user = crud_server.get_user(db, user_id=id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return crud_server.delete_user(db=db, user_id=id)