from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import slice as crud_slice
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/slices",
    tags=["slices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Slice])
async def read_slices(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    slices = crud_slice.get_slices(db, skip=skip, limit=limit)
    return slices

@router.get("/{id}",response_model=schema.Slice)
async def read_slice(id: int, db=Depends(get_db)):
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    return db_slice

@router.post("/", response_model=schema.Slice)
async def create_slice(slice: schema.SliceBase, db=Depends(get_db)):
    db_slice = crud_slice.get_slice_by_name(db,name=slice.name)
    if db_slice:
        raise HTTPException(status_code=40, detail="There is already a slice with that name")
    return crud_slice.create_slice(db=db, slice=slice)

@router.delete("/{id}")
async def delete_slice(id: str,db=Depends(get_db)):
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    return crud_slice.delete_slice(db=db, slice_id=id)