from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    id_port0 = Column(Integer, ForeignKey('ports.id'))
    id_port1 = Column(Integer, ForeignKey('ports.id'))

    port0 = relationship('Port', back_populates='links')
    port1 = relationship('Port', back_populates='links')

