from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from services.database import Base
import enum


class AvailabilityZone(Base):
    __tablename__ = "availability_zone"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    latitude = Column(String(20))
    longitude = Column(String(20))

    slices = relationship("Slice", back_populates="az")
    servers = relationship("Server", back_populates="az")




