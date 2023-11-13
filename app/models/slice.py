from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base
import enum
from datetime import datetime

class Topology(enum.Enum):
    arbol = "arbol"
    malla = "malla"
    bus = "bus"
    lineal = "lineal"
    anillo = "anillo"
    custom = "custom"

class Status(enum.Enum):
    creating = "creating"
    running = "running"
    stopped = "stopped"
    failed = "failed"
    not_deployed = "not_deployed"
    

class Slice(Base):
    __tablename__ = "slices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    topology = Column(Enum(Topology))
    status = Column(Enum(Status),default=Status.not_deployed)
    creationdate = Column(DateTime, default=datetime.now)
    id_az = Column(Integer, ForeignKey("availability_zone.id"))

    az = relationship("AvailabilityZone", back_populates="slices")

    users = relationship("SliceUser", back_populates="slice")
    nodes = relationship("Node", back_populates="slice")


