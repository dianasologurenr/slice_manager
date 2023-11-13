from pydantic import BaseModel
import enum


class UserBase(BaseModel):
    name: str
    email: str
    username: str

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

class Slice(SliceBase):
    id: int
    creationdate: str
    users: list[User] = []

    