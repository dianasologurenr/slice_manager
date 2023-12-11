from models.user import User
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

# Create Tables
Base.metadata.create_all(bind=engine)

# Migration
session = SessionLocal()

## AvailabilityZone
zone1 = AvailabilityZone(name="Worker1", latitude=18.21329, longitude=78.89518)
session.add(zone1)
zone2 = AvailabilityZone(name="Worker2", latitude=26.68452, longitude=117.75975)
session.add(zone2)
zone3 = AvailabilityZone(name="Worker3", latitude=12.68452, longitude=77.75975)
session.add(zone3)

## Slice
new_slice = Slice(
    name = "Slice Default",
    topology = "lineal",
    status = "not_deployed",
    az=zone1
)
session.add(new_slice)

## User
new_admin_1 = User(
    name="Miguel Ahumada",
    email="ahumadac.m@pucp.edu.pe",
    username="20190050",
    password="1234",
    role="admin"
)
session.add(new_admin_1)
new_admin_2 = User(
    name="Diana Sologuren",
    email="sologurenr.d@pucp.edu.pe",
    username="20185521",
    password="1234",
    role="admin"
)
session.add(new_admin_2)
new_admin_3 = User(
    name="Angie Alejandro",
    email="a20191792@pucp.edu.pe",
    username="20191792",
    password="1234",
    role="admin"
)
session.add(new_admin_3)

## SliceUser
new_slice_user = SliceUser(user=new_admin_2, slice=new_slice)
session.add(new_slice_user)

## Servers
worker1 = Server(
    core= 5,
    ram = 5,
    disk = 10,
    ip = "10.0.0.30",
    usage = 0.3,
    az=zone1)
session.add(worker1)
worker2 = Server(
    core= 5,
    ram = 5,
    disk = 10,
    ip = "10.0.0.40",
    usage = 0.3,
    az=zone2)
session.add(worker2)
worker3 = Server(
    core= 5,
    ram = 5,
    disk = 10,
    ip = "10.0.0.50",
    usage = 0.3,
    az=zone3)
session.add(worker3)

# ## Alerts
# alert_type1= Alert(
#     name = "Carga de CPU",
#     description = "Uso de CPU superior al umbral establecido"
# )
# session.add(alert_type1)
# alert_type2= Alert(
#     name = "Memoria RAM",
#     description = "Uso de memoria cerca del límite máximo"
# )
# session.add(alert_type2)
# alert_type3= Alert(
#     name = "Alamacenamiento",
#     description = "Espacio de almacenamiento agotado o casi agotado",
#     priority = "alta"
# )
# session.add(alert_type3)

# ## Monitoreo
# alert1 = Monitoreo(
#     server=worker1,
#     alert=alert_type1
# )
# session.add(alert1)
# alert2 = Monitoreo(
#     server=worker2,
#     alert=alert_type2
# )
# session.add(alert2)
# alert3 = Monitoreo(
#     server=worker3,
#     alert=alert_type3
# )
# session.add(alert3)

## Images
image1 = Image (
    name="Ubuntu 20.04 LTS",
    description="Distribución de Linux",
    path="/path/to/ubuntu2004.img",
    status="disponible"
)
session.add(image1)
image2 = Image (
    name="Windows Server 2019",
    description="Windows versión base",
    path="/path/to/win2019.img",
    status="disponible"
)
session.add(image2)

# ## Flavors
# flavor1 = Flavor(
#     core=2,
#     ram=4,
#     disk=100
# )
# session.add(flavor1)
# flavor2 = Flavor(
#     core=2,
#     ram=8,
#     disk=200
# )
# session.add(flavor2)
# flavor3 = Flavor(
#     core=1,
#     ram=2,
#     disk=50
# )
# session.add(flavor3)

## Security Groups
sg1_all = Security(
    name = "Default",
    description = "Default Security Group"
)
session.add(sg1_all)

## Inbound and Outbound Rules

## Nodes
node1 = Node (
    name= "VM_1",
    internetaccess= 0,
    image= None,
    flavor= None,
    slice= new_slice,
    server= worker1,
    security= sg1_all
)
session.add(node1)
node2 = Node (
    name= "VM_2",
    internetaccess= 0,
    image= None,
    flavor= None,
    slice= new_slice,
    server= worker1,
    security= sg1_all
)
session.add(node2)

## Ports
port1 = Port(
    name= "port_0",
    node= node1
)
session.add(port1)
port2 = Port(
    name= "port_0",
    node= node2
)
session.add(port2)

## Links
new_link = Link(
    port0=port1,
    port1=port2 
)
session.add(new_link)


# Creat Data
session.commit()