from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from services.database import Base

class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

    @validates('rol')
    def validate_role(self, key, value):
        allowed_values = ["admin", "user"]
        if value not in allowed_values:
            raise ValueError("El valor de 'role' no es válido.")
        return value