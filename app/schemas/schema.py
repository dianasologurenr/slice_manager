from typing import Optional
from pydantic import BaseModel
import enum
from datetime import datetime



class UserBase(BaseModel):
    name: str
    email: str
    username: str

class AvailabilityZoneBase(BaseModel):
    id: int


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class SliceBase(BaseModel):
    name: str
    

class Slice(SliceBase):
    id: int
    topology: Optional[str] = None
    status: Optional[str] = None
    creationdate: datetime
    id_az: Optional[int] = None
    az: Optional[str] = None
    nodes: int

    users: list[User] = []

    class Config:
        from_attributes = True

class NodeBase(BaseModel):
    name: str
    id_slice: int

class PortBase(BaseModel):
    name: str
    id_node: int

class LinkBase(BaseModel):
    id_port0: int
    id_port1: int

class FlavorBase(BaseModel):
   core: int
   ram: float
   disk: float

class Flavor(FlavorBase):
    id:int



class AvailabilityZone(AvailabilityZoneBase):
    name: str
    latitude: float
    longitude: float
    slices: list[Slice] = []

    class Config:
        from_attributes = True

class inBoundBase(BaseModel):
    protocol: str
    ports: str
    source: str
    description: str
    id_security: int
    

class inBound(inBoundBase):
    id: int
    security_name: Optional[str]

    class Config:
        from_attributes = True


class outBoundBase(BaseModel):
    protocol: str
    ports: str
    source: str
    description: str
    id_security: int

class outBound(inBoundBase):
    id: int
    security_name: Optional[str]
    
    class Config:
        from_attributes = True

class SecurityGroupBase(BaseModel):
    name: str
    description: str

class SecurityGroup(SecurityGroupBase):
    id: int
    inbounds: list[inBound] = []
    outbounds: list[outBound] = []

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    name: str
    description: Optional[str]=None

class Image(ImageBase):
    id: int
    path: str
    status: str
class ImageUpdate(BaseModel):
    status: Optional[str]=None
    path: Optional[str]=None

class SliceUpdate(BaseModel):
    topology: Optional[str] = None
    status: Optional[str] = None
    id_az: Optional[int] = None

class ServerBase(BaseModel):
    core: int
    ram: float
    disk: float
    ip: str
    id_az: int

class Server(ServerBase):
    id: int
    usage: float

    class Config:
        from_attributes = True

class Port(PortBase):
    id: int

    class Config:
        from_attributes = True
class Node(NodeBase):
    id: int
    internetaccess: Optional[int] = None
    id_image: Optional[int] = None
    id_server: Optional[int] = None
    id_security: Optional[int] = None
    id_flavor: Optional[int] = None

    image: Optional[str] = None
    flavor: Optional[Flavor] = None
    server: Optional[str] = None
    security: Optional[str] = None

    ports: list[Port] = []

    class Config:
        from_attributes = True

class NodeUpdate(BaseModel):
    internetaccess: Optional[int] = None
    id_image: Optional[int] = None
    id_server: Optional[int] = None
    id_security: Optional[int] = None
    id_flavor: Optional[int] = None

class Link(LinkBase):
    id: int
    port0: Optional[Port] = None
    port1: Optional[Port] = None

    class Config:
        from_attributes = True

class SliceUserBase(BaseModel):
    id_slice: int
    id_user: int

class SliceUser(SliceUserBase):

    class Config:
        from_attributes = True