from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from crud import availability_zone as crud_availability_zone
import schemas.schema as schema
from typing import List

router = APIRouter(
    prefix="/availability_zones",
    tags=["availability_zones"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.AvailabilityZone])
async def read_availability_zone(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    availability_zones = crud_availability_zone.get_availability_zone(db, skip=skip, limit=limit)
    return availability_zones




