from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import images as crud_image
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Image])
async def read_images(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    images = crud_image.get_image(db, skip=skip, limit=limit)
    return images

@router.get("/{id}",response_model=schema.Image)
async def read_image(id: int, db=Depends(get_db)):
    db_image = crud_image.get_image(db, id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.post("/", response_model=schema.Image)
async def create_image(image: schema.ImageBase, db=Depends(get_db)):
    db_image = crud_image.get_image_by_name(db,name=image.name)
    if db_image:
        raise HTTPException(status_code=40, detail="Name already registered")
    return crud_image.create_image(db=db, image=image)

@router.delete("/{id}")
async def delete_image(id: str,db=Depends(get_db)):
    db_image = crud_image.get_image(db, id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return crud_image.delete_image(db=db, id=id)