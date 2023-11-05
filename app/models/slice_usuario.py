from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Role(enum.Enum):
    admin = "admin",
    user = "user"

class SliceUsuario(Base):
    __tablename__ = "slice_users"

    id_slice = Column(Integer, ForeignKey("slices.id"),primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"), primary_key=True)

    user = relationship("Usuario", back_populates="slices")
    slice = relationship("Slice", back_populates="users")
