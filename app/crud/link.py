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

def get_links(db: Session, skip: int = 0, limit: int = 100):
    db_links = db.query(models_link.Link).offset(skip).limit(limit).all()
    links = [convert_sqlalchemy_to_pydantic(db_link) for db_link in db_links]
    return links

def get_link(db: Session, id: int):
    link = db.query(models_link.Link).filter(models_link.Link.id == id).first()
    return convert_sqlalchemy_to_pydantic(link)

def get_link_by_port(db: Session, id_port: int):
    link = db.query(models_link.Link).filter(or_(models_link.Link.id_port0 == id_port, 
                                                 models_link.Link.id_port1 == id_port)).first()
    return convert_sqlalchemy_to_pydantic(link)

def create_link(db: Session, link: schema.LinkBase):
    db_link = models_link.Link(
        id_port0 = link.id_port0,
        id_port1 = link.id_port1,
        )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return convert_sqlalchemy_to_pydantic(db_link)

def delete_link(db: Session, id: int):
    db_link = db.query(models_link.Link).filter(models_link.Link.id == id).first()
    db.delete(db_link)
    db.commit()
    return {"message": "Link deleted successfully"}

def convert_sqlalchemy_to_pydantic(Link: models_link.Link) -> schema.Link:
    if Link:
        return schema.Link(
            id=Link.id,
            id_port0=Link.id_port0,
            id_port1=Link.id_port1
        )
    return None