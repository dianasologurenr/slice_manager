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


def get_security_groups(db: Session, skip: int = 0, limit: int = 100):
    db_security_groups = db.query(models_security.Security).offset(skip).limit(limit).all()
    security_groups = [convert_sqlalchemy_user_to_pydantic(db_security_group) for db_security_group in db_security_groups]
    return security_groups

def create_security_groups(db: Session, security_group: schema.SecurityGroupBase):
    db_security_groups = models_security.Security(
            name=security_group.name, 
            description=security_group.description,
        )
    db.add(db_security_groups)
    db.commit()
    db.refresh(db_security_groups)
    return convert_sqlalchemy_user_to_pydantic(db_security_groups)

def get_security_group_by_name(db: Session, name: str):
    user = db.query(models_security.Security).filter(models_security.Security.name == name).first()
    return user

def get_security_group_by_id(db: Session, id: int):
    sg = db.query(models_security.Security).filter(models_security.Security.id == id).first()
    return convert_sqlalchemy_user_to_pydantic(sg)

def delete_security_groups(db: Session, security_group_id: int):
    db_security_groups = db.query(models_security.Security).filter(models_security.Security.id == security_group_id).first()
    db.delete(db_security_groups)
    db.commit()
    return {"message": "Security group deleted successfully"}


def convert_sqlalchemy_user_to_pydantic(security_group: models_security.Security) -> schema.SecurityGroup:
    
    inbounds = []
    for rule in security_group.inbound:
        inbounds.append(
            schema.inBound(
                id=rule.id,
                description=rule.description,
                protocol=rule.protocol.value,
                ports=rule.ports,
                source=rule.source,
                id_security=security_group.id,
                security_name=security_group.name
            )
        )

    outbounds = []
    for rule in security_group.outbound:
        outbounds.append(
            schema.outBound(
                id=rule.id,
                description=rule.description,
                protocol=rule.protocol.value,
                ports=rule.ports,
                source=rule.source,
                id_security=security_group.id,
                security_name=security_group.name
            )
        )

    return schema.SecurityGroup(
        id = security_group.id,
        name = security_group.name,
        description = security_group.description,
        inbounds= inbounds,
        outBounds= outbounds
    )