from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Role(enum.Enum):
    admin = "admin",
    user = "user"

class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(Role), default=Role.user)

    slices = relationship("SliceUsuario", back_populates="user")

