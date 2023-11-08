from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from services.database import Base
import enum
from datetime import datetime

class Monitoreo(Base):
    __tablename__ = "monitoreo"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now)
    id_alert = Column(Integer, ForeignKey("alerts.id"))
    id_server = Column(Integer, ForeignKey("servers.id"))

    server = relationship("Server", back_populates="alerts")
    alert = relationship("Alert", back_populates="servers")