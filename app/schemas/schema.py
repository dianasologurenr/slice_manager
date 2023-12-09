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
    security_name: Optional[str]

class inBound(inBoundBase):
    id: int

class outBoundBase(BaseModel):
    protocol: str
    ports: str
    source: str
    description: str
    id_security: int
    security_name: Optional[str]

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


class Node(NodeBase):
    id: int
    image: str
    flavor: Flavor
    server: str
    security: str
    internetaccess: int = 0
    id_slice: Optional[int]
    id_image: Optional[int]
    id_server: Optional[int]
    id_security: Optional[int]
    id_flavor: Optional[int]
    class Config:
        from_attributes = True