from pydantic import BaseModel


class SliceBase(BaseModel):
    name: str
    topologia: str = 'arbol, malla, bus, lineal, anillo'
    estado: str = 'corriendo', 'detenido', 'error'

class SliceCreate(UserBase):
    fechacreacion: str
    idZonaDisponibilidad: int

class Slice(UserBase):
    id: int
    

