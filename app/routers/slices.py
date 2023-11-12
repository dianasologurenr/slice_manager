from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import slices as crud_slices
from schemas import schemas_slices

router = APIRouter(
    prefix="/slices",
    tags=["slices"],
    responses={404: {"description": "Not found"}},
)

"""@router.get("/",response_model=list[schemas_user.User])
async def read_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{id}",response_model=schemas_user.User)
async def read_user(id: int, db=Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @router.put("/{id}")
# async def update_user(id: str):
#     if id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"name": fake_items_db[id]["name"], "id": id}

@router.post("/{id}", response_model=schemas_user.User)
async def create_user(user: schemas_user.UserCreate, db=Depends(get_db)):
    db_user = crud_user.get_user_by_username(db,username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user) """

