from models import user as models_user
from models.slice import Slice
from models.slice_user import SliceUser
from models.availability_zone import AvailabilityZone
from models.server import Server
from models.alerts import Alert
from models.monitoreo import Monitoreo
from models.image import Image
from models.flavor import Flavor
from models.node import Node
from models.security import Security
from models.inbound import Inbound
from models.outbound import Outbound
from models.port import Port
from models.link import Link

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.database import Base, engine, SessionLocal
from config import SQLALCHEMY_DATABASE_URL
from datetime import datetime

# Migration
db = SessionLocal()
skip = 0
limit = 100
users = db.query(models_user.User).offset(skip).limit(limit).all()

print(users)