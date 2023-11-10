from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from services.database import Base


class Security(Base):
    __tablename__ = "security"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))
    description = Column(String(100))

    nodes = relationship("Node", back_populates="security")
    
    inbound = relationship("Inbound", back_populates="security")
    outbound = relationship("Outbound", back_populates="security")