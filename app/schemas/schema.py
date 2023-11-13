from pydantic import BaseModel
import enum

class SliceBase(BaseModel):
    name: str
    topology: str
    status: str
    creationdate: str

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

class AvailabilityZone(AvailabilityZoneBase):
    name: str
    latitude: float
    longitude: float

class SecurityGroup(SecurityGroupBase):
    name: str
    description: str

class SecurityGroupCreate(SecurityGroupBase):
    name: str
    description: str

# class Slice(UserBase):
#     id: int
#     users: list[User] = []

# class SliceCreate(UserBase):
#     password: str