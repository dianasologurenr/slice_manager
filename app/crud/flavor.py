from sqlalchemy.orm import Session
from sqlalchemy import select
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
    flavors = [convert_sqlalchemy_to_pydantic(db_flavor) for db_flavor in db_flavors]
    return flavors

def get_flavor(db: Session, flavor_id: int):
    flavor = db.query(models_flavor.Flavor).filter(models_flavor.Flavor.id == flavor_id).first()
    return convert_sqlalchemy_to_pydantic(flavor)

def create_flavor(db: Session, flavor: schema.FlavorBase):
    db_flavor = models_flavor.Flavor(
        core = flavor.core,
        ram = flavor.ram,
        disk = flavor.disk
    )
    db.add(db_flavor)
    db.commit()
    db.refresh(db_flavor)
    return convert_sqlalchemy_to_pydantic(db_flavor)

def delete_flavor(db: Session, flavor_id: int):
    db_flavor = db.query(models_flavor.Flavor).filter(models_flavor.Flavor.id == flavor_id).first()
    db.delete(db_flavor)
    db.commit()
    return {"message": "Flavor deleted successfully"}


def get_flavors_by_id_slice(db: Session, id_slice: int):
    # Define la consulta
    query = select(
            models_flavor.Flavor.id, 
            models_flavor.Flavor.core, 
            models_flavor.Flavor.ram, 
            models_flavor.Flavor.disk
        ) \
        .select_from(models_node.Node) \
        .join(models_flavor.Flavor, models_flavor.Flavor.id == models_node.Node.id_flavor, isouter=True) \
        .where(models_node.Node.id_slice == id_slice)

    # Ejecuta la consulta
    result = db.execute(query).fetchall()

    return result


def convert_sqlalchemy_to_pydantic(flavor: models_flavor.Flavor) -> schema.Flavor:
    if flavor: 
        return schema.Flavor(
            id=flavor.id,
            core=flavor.core,
            ram=flavor.ram,
            disk=flavor.disk
        )
    return None