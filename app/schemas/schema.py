from pydantic import BaseModel
import enum
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    username: str

class AvailabilityZoneBase(BaseModel):
    id: int


class SecurityGroupBase(BaseModel):
    name: str
    description: str

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

class AvailabilityZone(AvailabilityZoneBase):
    name: str
    latitude: float
    longitude: float
    slices: list[Slice] = []

    class Config:
        from_attributes = True

class SecurityGroup(SecurityGroupBase):
    id: int






# class Slice(UserBase):
#     id: int
#     users: list[User] = []



    