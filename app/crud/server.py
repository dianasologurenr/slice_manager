from sqlalchemy.orm import Session

from models import user as models_
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

def get_servers(db: Session, skip: int = 0, limit: int = 100):
    db_servers = db.query(models_server.Server).offset(skip).limit(limit).all()
    servers = [convert_sqlalchemy_to_pydantic(db_server) for db_server in db_servers]
    return servers

def get_server(db: Session, id: int):
    server = db.query(models_server.Server).filter(models_server.Server.id == id).first()
    return convert_sqlalchemy_to_pydantic(server)

# def update_server(db: Session, server: schema.Server):
#     db_user = db.query(models_user.User).filter(models_user.User.id == user_id).first()
#     db.delete(db_user)
#     db.commit()
#     return {"message": "User deleted successfully"}
    
    
#     db_user = models_server.User(
#         name=server.name,
#         email=server.email, 
#         username=server.username,
#         password=fake_hashed_password
#         )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return convert_sqlalchemy_to_pydantic(db_user)

def convert_sqlalchemy_to_pydantic(server: models_server.Server) -> schema.Server:
    if server:
        return schema.Server(
            core=server.core,
            ram=server.ram,
            disk=server.disk,
            ip=server.ip,
            id_az=server.id_az,
            id=server.id,
            usage=server.usage
        )
    return None