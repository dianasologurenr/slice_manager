from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base
import enum

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    internetaccess = Column(Integer)
    id_slice = Column(Integer, ForeignKey("slices.id"))
    id_image = Column(Integer, ForeignKey("images.id"))
    id_server = Column(Integer, ForeignKey("servers.id"))
    id_security = Column(Integer, ForeignKey("security.id"))
    id_flavor = Column(Integer, ForeignKey("flavors.id"))

    image = relationship("Images", back_populates="nodes")
    flavor = relationship("Flavor", back_populates="nodes")
    slice = relationship("Slice", back_populates="nodes")
    server = relationship("Server", back_populates="nodes")
    security = relationship("Security", back_populates="nodes")

    ports = relationship("Port", back_populates="node")

    





