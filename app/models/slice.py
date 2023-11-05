from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from services.database import Base
import enum
from datetime import datetime

class Topology(enum.Enum):
    arbol = "arbol",
    malla = "malla",
    bus = "bus",
    lineal = "lineal",
    anillo = "anillo"

class State(enum.Enum):
    running = "running",
    stopped = "stopped",
    failed = "failed"
    

class Slice(Base):
    __tablename__ = "slices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    topology = Column(Enum(Topology))
    state = Column(Enum(State))
    creationdate = Column(DateTime, default=datetime.now)

    users = relationship("SliceUsuario", back_populates="slice")

