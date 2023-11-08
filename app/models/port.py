from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base


class Port(Base):
    __tablename__ = 'ports'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    id_node = Column(Integer, ForeignKey('nodes.id')) 
    
    links = relationship('Link', primaryjoin='or_(Port.id==Link.id_port0, Port.id==Link.id_port1)')




