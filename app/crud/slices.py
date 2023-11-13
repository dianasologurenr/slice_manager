from sqlalchemy.orm import Session

from models import user as models_user
from models import slice_user as models_slice_user
from models import slice as models_slice
from models import availability_zone as models_availability_zone
from models import node as models_node
from models import server as models_server
from models import image as models_image
from models import flavor as models_flavor
from models import security as models_security
from models import port as models_port
from models import link as models_link
from models import monitoreo as models_monitoreo
from models import inbound as models_inbound
from models import outbound as models_outbound
from models import alerts as models_alerts
from schemas import schema

def get_slices(db: Session, skip: int = 0, limit: int = 100):
    db_slices = db.query(models_slice.Slice).offset(skip).limit(limit).all()
    slices = [convert_sqlalchemy_slice_to_pydantic(db_slice) for db_slice in db_slices]
    return slices

def get_slice(db: Session, slice_id: int):
    slice = db.query(models_slice.Slice).filter(models_slice.Slice.id == slice_id).first()
    return convert_sqlalchemy_slice_to_pydantic(slice)

def get_slice_by_name(db: Session, name: str):
    slice = db.query(models_slice.Slice).filter(models_slice.Slice.name == name).first()
    return slice

def create_slice(db: Session, slice: schema.SliceCreate):
    db_slice = models_slice.Slice(
        name=slice.name,
        status=slice.status,
        creationdate=slice.creationdate
        )
    db.add(db_slice)
    db.commit()
    db.refresh(db_slice)
    return convert_sqlalchemy_slice_to_pydantic(db_slice)

def delete_slice(db: Session, slice_id: int):
    db_slice = db.query(models_slice.Slice).filter(models_slice.Slice.id == slice_id).first()
    db.delete(db_slice)
    db.commit()
    return {"message": "Slice deleted successfully"}


def convert_sqlalchemy_slice_to_pydantic(slice: models_slice.Slice) -> schema.Slice:
    return schema.Slice(
        id=slice.id,
        name=slice.name,
        status=slice.status,
        creationdate=slice.creationdate
    )