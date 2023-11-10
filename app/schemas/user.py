from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    username: str
    role: str = 'user'

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    # items: list[Slice] = []

