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

def get_outbound(db: Session, skip: int = 0, limit: int = 100):
    db_outbounds = db.query(models_outbound.Outbound).offset(skip).limit(limit).all()
    outbounds = [convert_sqlalchemy_outbound_to_pydantic(db_outbound) for db_outbound in db_outbounds]
    return outbounds

def convert_sqlalchemy_outbound_to_pydantic(outbound: models_outbound.Outbound) -> schema.outBound:
    if outbound: 
        return schema.outBound(
            id=outbound.id,
            protocol=outbound.protocol.value,
            ports=outbound.ports,
            source=outbound.source,
            description=outbound.description,
            id_security=outbound.id_security,
            security_name=outbound.security.name  
        )
    return None


def create_outbound(db: Session, outbound: schema.outBoundBase):
    db_outbound = models_outbound.Outbound(
            protocol = outbound.protocol,
            ports = outbound.ports,
            source = outbound.source,
            description = outbound.description,
            id_security = outbound.id_security
        )
    db.add(db_outbound)
    db.commit()
    db.refresh(db_outbound)
    return convert_sqlalchemy_outbound_to_pydantic(db_outbound)

def get_outbound_byID(db: Session, outbound_id: int):
    outbound = db.query(models_outbound.Outbound).filter(models_outbound.Outbound.id == outbound_id).first()
    return convert_sqlalchemy_outbound_to_pydantic(outbound)

def get_outbound_byIdSecurity(db: Session, outbound_idSecurity: int ,skip: int = 0, limit: int = 100):
    db_outbounds = db.query(models_outbound.Outbound).filter(models_outbound.Outbound.id_security == outbound_idSecurity).offset(skip).limit(limit).all()
    outbounds = [convert_sqlalchemy_outbound_to_pydantic(db_outbound) for db_outbound in db_outbounds]
    return convert_sqlalchemy_outbound_to_pydantic(outbounds)

def delete_outbound(db: Session, outbound_id: int):
    db_outbound = db.query(models_outbound.Outbound).filter(models_outbound.Outbound.id == outbound_id).first()
    db.delete(db_outbound)
    db.commit()
    return {"message": "Outbound deleted successfully"}


