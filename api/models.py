from datetime import datetime
from pydantic import BaseModel, condecimal


class CreateProduct(BaseModel):
    nombre: str
    descripcion: str
    precio: condecimal(max_digits=12, decimal_places=2)
    imagen: str
    class Config:
        orm_mode = True
        title = "CreateProduct"


class ReadProduct(CreateProduct):
    id: int
    class Config:
        orm_mode = True
        title = "ReadProduct"

class ReadPago(BaseModel):
    id:int
    fecha_pago: datetime
    fecha_validacion: datetime | None
    monto: float
    validado: bool