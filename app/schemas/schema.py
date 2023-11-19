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
    id_az: int
    name: str
    topology: str

class Slice(SliceBase):
    id: int
    status: str
    creationdate: datetime
    users: list[User] = []

class NodeBase(BaseModel):
    name: str
    id_slice: int
    id_image: int
    id_server: int
    id_security: int
    id_flavor: int

class Node(NodeBase):
   id: int
   internetaccess: int
   users: list[User] = []

class FlavorBase(BaseModel):
   core: int
   ram: float
   disk: float

class Flavor(FlavorBase):
    id:int
    users: list[User] = []



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

class outBoundBase(BaseModel):
    protocol: str
    ports: str
    source: str
    description: str
    id_security: int

class outBound(inBoundBase):
    id: int

class SecurityGroupBase(BaseModel):
    name: str
    description: str

class SecurityGroup(SecurityGroupBase):
    id: int
    inbounds: list[inBound] = []
    outBounds: list[outBound] = []

    class Config:
        from_attributes = True







# class Slice(UserBase):
#     id: int
#     users: list[User] = []





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