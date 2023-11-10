from sqlalchemy.orm import Session

from models import user as models_user
from schemas import user as schemas_user


def get_user(db: Session, user_id: int):
    return db.query(models_user.User).filter(models_user.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models_user.User).filter(models_user.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas_user.UserCreate):
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
    return db_user


