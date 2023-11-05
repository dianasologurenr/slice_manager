from models.usuario import Usuario
from models.slice import Slice
from models.slice_usuario import SliceUsuario
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

new_user = Usuario(
    name = "diana",
    email = "diana@gmail.com",
    username = "dianasologuren",
    password = "1234",
    role = "user")
session.add(new_user)

new_slice_user = SliceUsuario(user=new_user, slice=new_slice)
session.add(new_slice_user)


session.commit()