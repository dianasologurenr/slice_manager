from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import user as crud_user
from crud import slice_user as crud_slice_user
import schemas.schema as schema
from typing import List
from services import funciones as openstack
from config import GATEWAY_IP, ADMIN_PASSWORD, ADMIN_PROJECT_NAME, ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_USERNAME,ADMIN_ID,ADMIN,READER,MEMBER,IP_VERSION, CIDR, IMAGEN_ID

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.User])
async def read_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{id}/",response_model=schema.User)
async def read_user(id: int, db=Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/role/{role}/",response_model=List[schema.User])
async def read_users_by_role(role:str, skip: int = 0, limit: int = 100, db=Depends(get_db)):
    users = crud_user.get_users_by_rol(db, role=role, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db=Depends(get_db)):
    db_user = crud_user.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    temp = crud_user.get_user_by_username(db,username=user.username)
    if temp:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    try:
        # create user with openstack
        admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP,ADMIN_PASSWORD,ADMIN_USERNAME,ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_PROJECT_NAME)
        if admin_token:
            username = user.username
            password = user.password
            email = user.email  
            new_user = openstack.crearUsuario(GATEWAY_IP,admin_token,username,password,email)
            if new_user:
                print(new_user)
                # create user in database
                return crud_user.create_user(db=db, user=user)

        raise HTTPException(status_code=400, detail="Error while creating user")    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error while creating user")

@router.delete("/{id}")
async def delete_user(id: str,db=Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    slice_user = crud_slice_user.get_slice_user_by_user(db, user_id=id)
    if slice_user:
        raise HTTPException(status_code=400, detail="User is associated with a slice")
    try:
        # create user with openstack
        admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP,ADMIN_PASSWORD,ADMIN_USERNAME,ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_PROJECT_NAME)
        if admin_token:
            user_id = openstack.obtenerIdUsuario(GATEWAY_IP, admin_token, db_user.username)
            if user_id:
                deleted = openstack.eliminarUsuario(GATEWAY_IP, admin_token, user_id)
                if deleted:
                    return crud_user.delete_user(db=db, user_id=id)

        raise HTTPException(status_code=400, detail="Error while deleting user")    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error while deleting user")
    