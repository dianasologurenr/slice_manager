from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base


class Port(Base):
    __tablename__ = 'ports'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    id_node = Column(Integer, ForeignKey('nodes.id')) 
    
    node = relationship("Node", back_populates="ports")

    links_as_port0 = relationship('Link', 
                                  primaryjoin='Port.id==Link.id_port0',
                                  back_populates='port0')
    links_as_port1 = relationship('Link', 
                                  primaryjoin='Port.id==Link.id_port1',
                                  back_populates='port1')




