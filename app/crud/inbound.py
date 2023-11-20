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

def get_inbound(db: Session, skip: int = 0, limit: int = 100):
    db_inbounds = db.query(models_inbound.Inbound).offset(skip).limit(limit).all()
    inbounds = [convert_sqlalchemy_inbound_to_pydantic(db_inbound) for db_inbound in db_inbounds]
    return inbounds

def convert_sqlalchemy_inbound_to_pydantic(inbound: models_inbound.Inbound) -> schema.inBound:
    if inbound: 
        return schema.inBound(
            id=inbound.id,
            protocol=inbound.protocol.value,
            ports=inbound.ports,
            source=inbound.source,
            description=inbound.description,
            id_security=inbound.id_security,
            security_name=inbound.security.name  
        )
    return None

def create_inbound(db: Session, inbound: schema.inBoundBase):
    db_inbound = models_inbound.Inbound(
            protocol = inbound.protocol,
            ports = inbound.ports,
            source = inbound.source,
            description = inbound.description,
            id_security = inbound.id_security
        )
    db.add(db_inbound)
    db.commit()
    db.refresh(db_inbound)
    return convert_sqlalchemy_inbound_to_pydantic(db_inbound)

def get_inbound_byID(db: Session, inbound_id: int):
    inbound = db.query(models_inbound.Inbound).filter(models_inbound.Inbound.id == inbound_id).first()
    return convert_sqlalchemy_inbound_to_pydantic(inbound)

def get_inbound_byIdSecurity(db: Session, inbound_idSecurity: int ,skip: int = 0, limit: int = 100):
    db_inbounds = db.query(models_inbound.Inbound).filter(models_inbound.Inbound.id_security == inbound_idSecurity).offset(skip).limit(limit).all()
    inbounds = [convert_sqlalchemy_inbound_to_pydantic(db_inbound) for db_inbound in db_inbounds]
    return convert_sqlalchemy_inbound_to_pydantic(inbounds)

def delete_inbound(db: Session, inbound_id: int):
    db_inbound = db.query(models_inbound.Inbound).filter(models_inbound.Inbound.id == inbound_id).first()
    db.delete(db_inbound)
    db.commit()
    return {"message": "Inbound deleted successfully"}
