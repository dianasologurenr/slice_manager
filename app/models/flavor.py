from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Flavor(Base):
    __tablename__ = "flavors"

    id = Column(Integer, primary_key=True, index=True)
    core = Column(Integer)
    ram = Column(Float)
    disk = Column(Float)

    nodes = relationship("Node", back_populates="flavor")

