from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Protocol(enum.Enum):
    tcp = "tcp",
    udp = "udp",
    icmp = "icmp",
    all = 'all'


class Inbound(Base):
    __tablename__ = "inbound"

    id = Column(Integer, primary_key=True, index=True)
    protocol = Column(Enum(Protocol))
    ports = Column(String(45))
    source = Column(String(20))
    description = Column(String(255))
    id_security = Column(Integer, ForeignKey('security.id')) 

    security = relationship("Security", back_populates="inbound")

