from models.user import User
from models.slice import Slice
from models.slice_user import SliceUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.database import Base, engine, SessionLocal
from config import SQLALCHEMY_DATABASE_URL
from datetime import datetime


print(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

session = SessionLocal()

new_slice = Slice(
    name = "Test",
    topology = "arbol",
    state = "stopped"
)
session.add(new_slice)

new_user = User(
    name = "diana",
    email = "diana@gmail.com",
    username = "dianasologuren",
    password = "1234",
    role = "user")
session.add(new_user)

new_slice_user = SliceUser(user=new_user, slice=new_slice)
session.add(new_slice_user)


session.commit()