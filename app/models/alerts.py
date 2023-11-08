from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Priority(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))
    priority = Column(Enum(Priority), default=Priority.medium)

    servers = relationship("Monitoreo", back_populates="alert")


