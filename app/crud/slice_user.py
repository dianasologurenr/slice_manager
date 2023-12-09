from sqlalchemy import or_
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

def get_slice_users(db: Session, skip: int = 0, limit: int = 100):
    db_slice_user = db.query(models_slice_user.SliceUser).offset(skip).limit(limit).all()
    slice_users = [convert_sqlalchemy_to_pydantic(item) for item in db_slice_user]
    return slice_users

def get_slice_user(db: Session, slice_user: schema.SliceUserBase):
    slice_user = db.query(models_slice_user.SliceUser).filter(models_slice_user.SliceUser.id_slice==slice_user.id_slice,
                                                              models_slice_user.SliceUser.id_user==slice_user.id_user).first()
    return convert_sqlalchemy_to_pydantic(slice_user)

def create_slice_user(db: Session, slice_user: schema.SliceUserBase):
    db_slice_user = models_slice_user.SliceUser(
        id_slice = slice_user.id_slice,
        id_user= slice_user.id_user,
    )
    db.add(db_slice_user)
    db.commit()
    db.refresh(db_slice_user)
    return convert_sqlalchemy_to_pydantic(db_slice_user)

def delete_slice_user(db: Session, slice_user: schema.SliceUserBase):
    db_slice_user = db.query(models_slice_user.SliceUser).filter(models_slice_user.SliceUser.id_slice==slice_user.id_slice,
                                                              models_slice_user.SliceUser.id_user==slice_user.id_user).first()
    db.delete(db_slice_user)
    db.commit()
    return {"message": "Slice_User deleted successfully"}

def convert_sqlalchemy_to_pydantic(slice_user: models_slice_user.SliceUser) -> schema.SliceUser:
    if slice_user:
        return schema.SliceUser(
            id=slice_user.user.id,
            id_slice=slice_user.slice.id,
            id_user=slice_user.user.id,
        )
    return None