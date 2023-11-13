from pydantic import BaseModel
import enum


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
    name: str
    topology: str
    status: str
    
class AvailabilityZone(AvailabilityZoneBase):
    name: str
    latitude: float
    longitude: float

class SecurityGroup(SecurityGroupBase):
    name: str
    description: float

class SecurityGroupCreate(SecurityGroupBase):
    name: str
    description: float

# class Slice(UserBase):
#     id: int
#     users: list[User] = []

class Slice(SliceBase):
    id: int
    creationdate: str
    users: list[User] = []

    