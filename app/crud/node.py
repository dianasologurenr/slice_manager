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

def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    db_nodes = db.query(models_node.Node).offset(skip).limit(limit).all()
    nodes = [convert_sqlalchemy_node_to_pydantic(db_node) for db_node in db_nodes]
    return nodes

def get_nodes_by_slice(db: Session, slice_id: int, skip: int = 0, limit: int = 100):
    db_nodes = db.query(models_node.Node).filter(models_node.Node.id_slice == slice_id).offset(skip).limit(limit).all()
    nodes = [convert_sqlalchemy_node_to_pydantic(db_node) for db_node in db_nodes]
    return nodes

def get_node(db: Session, node_id: int):
    node = db.query(models_node.Node).filter(models_node.Node.id == node_id).first()
    return convert_sqlalchemy_node_to_pydantic(node)


def get_node_by_name_in_slice(db: Session, name: str, id_slice: int):
    node = db.query(models_node.Node).filter(models_node.Node.id_slice==id_slice, models_node.Node.name == name).first()
    return node

def create_node(db: Session, node: schema.NodeBase):
    db_node = models_node.Node(
        name=node.name,
        id_slice = node.id_slice,
        )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return convert_sqlalchemy_node_to_pydantic(db_node)

def delete_node(db: Session, node_id: int):
    db_node = db.query(models_node.Node).filter(models_node.Node.id == node_id).first()
    db.delete(db_node)
    db.commit()
    return {"message": "Node deleted successfully"}


def convert_sqlalchemy_node_to_pydantic(node: models_node.Node) -> schema.Node:
    if node:
        return schema.Node(
            id=node.id,
            name=node.name,
            internetaccess=node.internetaccess,
            id_slice=node.id_slice,
            id_image=node.id_image,
            id_server=node.id_server,
            id_security=node.id_security,
            id_flavor=node.id_flavor,
            image= node.image.name if node.image else None,
            flavor= schema.Flavor(
                id=node.flavor.id,
                core=node.flavor.core,
                ram=node.flavor.ram,
                disk=node.flavor.disk
            ) if node.flavor else None,
            server= node.server.ip if node.server else None,
            security= node.security.name if node.security else None,
            ports=[schema.Port(
                    id=port.id,
                    name=port.name,
                    id_node=port.id_node,
                ) for port in node.ports
            ] if node.ports else []
        )
    return None
