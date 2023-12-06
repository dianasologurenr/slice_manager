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

def get_ports(db: Session, skip: int = 0, limit: int = 100):
    db_ports = db.query(models_port.Port).offset(skip).limit(limit).all()
    ports = [convert_sqlalchemy_to_pydantic(db_port) for db_port in db_ports]
    return ports

def get_port(db: Session, id: int):
    port = db.query(models_port.Port).filter(models_port.Port.id == id).first()
    return convert_sqlalchemy_to_pydantic(port)

def get_ports_by_node(db: Session, id_node: int, skip: int = 0, limit: int = 100):
    db_ports = db.query(models_port.Port).filter(models_port.Port.id_node == id_node).offset(skip).limit(limit).all()
    ports = [convert_sqlalchemy_to_pydantic(db_port) for db_port in db_ports]
    return ports

def get_port_by_name_in_node(db: Session, name: str, id_node: int):
    port = db.query(models_port.Port).filter(models_port.Port.id_node == id_node, models_port.Port.name == name).first()
    return port

def create_port(db: Session, port: schema.PortBase):
    db_port = models_port.Port(
        name=port.name,
        id_node = port.id_node,
        )
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return convert_sqlalchemy_to_pydantic(db_port)

def delete_port(db: Session, id: int):
    db_port = db.query(models_port.Port).filter(models_port.Port.id == id).first()
    db.delete(db_port)
    db.commit()
    return {"message": "Port deleted successfully"}

def convert_sqlalchemy_to_pydantic(port: models_port.Port) -> schema.Port:
    if port:
        return schema.Port(
            id=port.id,
            name=port.name,
            id_node=port.id_node
        )
    return None