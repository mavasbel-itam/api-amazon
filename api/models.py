from pydantic import BaseModel, Field, condecimal
from datetime import datetime


class CreateProduct(BaseModel):
    nombre: str
    descripcion: str
    precio: condecimal(max_digits=12, decimal_places=2)
    imagen: str

    class Config:
        from_attributes = True
        title = "CreateProduct"


class ReadProduct(CreateProduct):
    id: int

    class Config:
        orm_mode = True
        title = "ReadProduct"


class BaseReadUser(BaseModel):
    id: int
    nombre: str
    apellido: str
    telefono: str
    correo: str
    es_prime: bool

    class Config:
        from_attributes = True
        title = "ReadUser"


class BaseReadOrder(BaseModel):
    id: int
    fecha_creacion: datetime
    fecha_entrega: datetime | None
    direccion_entrega: str

    class Config:
        from_attributes = True
        title = "ReadOrden"

class ReadOrderWithUser(BaseReadOrder):
    usuario: BaseReadUser

    class Config:
        from_attributes = True
        title = "ReadOrden"


class ReadUserWithOrders(BaseReadUser):
    ordenes: list[BaseReadOrder]

    class Config:
        from_attributes = True
        title = "ReadUserWithOrders"
        allow_population_by_field_name = True
