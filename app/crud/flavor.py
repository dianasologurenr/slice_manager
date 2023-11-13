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


def get_flavors(db: Session, skip: int = 0, limit: int = 100):
    db_flavors = db.query(models_flavor.Flavor).offset(skip).limit(limit).all()
    flavors = [convert_sqlalchemy_flavor_to_pydantic(db_flavor) for db_flavor in db_flavors]
    return flavors

def get_flavor(db: Session, flavor_id: int):
    flavor = db.query(models_flavor.Flavor).filter(models_flavor.Flavor.id == flavor_id).first()
    return convert_sqlalchemy_flavor_to_pydantic(flavor)

"""def create_slice(db: Session, slice: schema.SliceBase):
    db_slice = models_slice.Slice(
        name=slice.name,
        id_az=slice.id_az,
        topology=slice.topology
        )
    db.add(db_slice)
    db.commit()
    db.refresh(db_slice)
    return convert_sqlalchemy_flavor_to_pydantic(db_slice)"""

def delete_flavor(db: Session, flavor_id: int):
    db_flavor = db.query(models_flavor.Flavor).filter(models_flavor.Flavor.id == flavor_id).first()
    db.delete(db_flavor)
    db.commit()
    return {"message": "Flavor deleted successfully"}


def convert_sqlalchemy_flavor_to_pydantic(flavor: models_flavor.Flavor) -> schema.Flavor:
    if flavor: 
        return schema.Flavor(
            id=flavor.id,
            core=flavor.core,
            ram=flavor.ram,
            disk=flavor.disk
        )
    return None