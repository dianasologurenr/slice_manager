import os
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Status(enum.Enum):
    disponible = "disponible"
    descargando = "descargando"
    error = "error"


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(255),default=None)
    path = Column(String(100),default="")
    status = Column(Enum(Status), default=Status.descargando)

    nodes = relationship("Node", back_populates="image")

