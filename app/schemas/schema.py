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

class AvailabilityZone(AvailabilityZoneBase):
    name: str
    latitude: float
    longitude: float
    slices: list[Slice] = []

    class Config:
        from_attributes = True

class SecurityGroup(SecurityGroupBase):
    name: str
    description: float

class SecurityGroupCreate(SecurityGroupBase):
    name: str
    description: float

# class Slice(UserBase):
#     id: int
#     users: list[User] = []



    