from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    core = Column(Integer)
    ram = Column(Float)
    disk = Column(Float)
    ip = Column(String(15))
    usage = Column(Float)
    id_az = Column(Integer, ForeignKey("availability_zone.id"))

    az = relationship("AvailabilityZone", back_populates="servers")
    alerts = relationship("Monitoreo", back_populates="server")
    nodes = relationship("Node", back_populates="server")
    

    

