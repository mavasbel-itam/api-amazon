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
