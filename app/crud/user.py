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

def get_users(db: Session, skip: int = 0, limit: int = 100):
    db_users = db.query(models_user.User).offset(skip).limit(limit).all()
    users = [convert_sqlalchemy_user_to_pydantic(db_user) for db_user in db_users]
    return users

def get_user(db: Session, user_id: int):
    user = db.query(models_user.User).filter(models_user.User.id == user_id).first()
    return convert_sqlalchemy_user_to_pydantic(user)

def get_user_by_email(db: Session, email: str):
    user = db.query(models_user.User).filter(models_user.User.email == email).first()
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(models_user.User).filter(models_user.User.username == username).first()
    return user

def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models_user.User(
        name=user.name,
        email=user.email, 
        username=user.username,
        password=fake_hashed_password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return convert_sqlalchemy_user_to_pydantic(db_user)

def delete_user(db: Session, user_id: int):
    db_user = db.query(models_user.User).filter(models_user.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

def convert_sqlalchemy_user_to_pydantic(user: models_user.User) -> schema.User:
    if user:
        return schema.User(
            id=user.id,
            name=user.name,
            email=user.email,
            username=user.username,
            role=user.role.value  # Asumiendo que 'role' es un Enum de SQLAlchemy
        )
    return None