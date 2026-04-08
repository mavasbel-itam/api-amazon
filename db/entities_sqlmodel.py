from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ------------------------------
# Categoria
# ------------------------------
class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=300, nullable=False, unique=True)

    productos: List["ProductoCategoria"] = Relationship(
        back_populates="categoria"
    )


# ------------------------------
# Producto
# ------------------------------
class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=300, nullable=False)
    descripcion: str = Field(nullable=False)
    precio: float = Field(nullable=False)
    imagen: str = Field(max_length=100, nullable=False)

    categorias: List["ProductoCategoria"] = Relationship(
        back_populates="producto"
    )

    ordenes: List["ProductoOrden"] = Relationship(
        back_populates="producto"
    )


# ------------------------------
# Usuario
# ------------------------------
class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=300, nullable=False)
    apellido: str = Field(max_length=300, nullable=False)
    telefono: str = Field(max_length=15, nullable=False, unique=True)
    correo: str = Field(max_length=254, nullable=False, unique=True)
    contrasena: str = Field(max_length=100, nullable=False)
    es_prime: bool = Field(nullable=False)

    ordenes: List["Orden"] = Relationship(back_populates="usuario")


# ------------------------------
# Orden
# ------------------------------
class Orden(SQLModel, table=True):
    __tablename__ = "orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(nullable=False)
    fecha_entrega: Optional[datetime] = Field(default=None)
    direccion_entrega: str = Field(nullable=False)

    usuario_id: int = Field(foreign_key="usuario.id", nullable=False)

    usuario: Optional["Usuario"] = Relationship(back_populates="ordenes")
    pagos: List["Pago"] = Relationship(back_populates="orden")
    productos: List["ProductoOrden"] = Relationship(back_populates="orden")


# ------------------------------
# Pago
# ------------------------------
class Pago(SQLModel, table=True):
    __tablename__ = "pago"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_pago: datetime = Field(nullable=False)
    fecha_validacion: Optional[datetime] = Field(default=None)
    monto: float = Field(nullable=False)
    validado: bool = Field(nullable=False)

    orden_id: int = Field(foreign_key="orden.id", nullable=False)

    orden: Optional["Orden"] = Relationship(back_populates="pagos")


# ------------------------------
# ProductoCategoria (Association Object)
# ------------------------------
class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    id: Optional[int] = Field(default=None, primary_key=True)

    categoria_id: int = Field(foreign_key="categoria.id", nullable=False)
    producto_id: int = Field(foreign_key="producto.id", nullable=False)

    categoria: Optional["Categoria"] = Relationship(back_populates="productos")
    producto: Optional["Producto"] = Relationship(back_populates="categorias")


# ------------------------------
# ProductoOrden (Association Object)
# ------------------------------
class ProductoOrden(SQLModel, table=True):
    __tablename__ = "producto_orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: int = Field(nullable=False)

    orden_id: int = Field(foreign_key="orden.id", nullable=False)
    producto_id: int = Field(foreign_key="producto.id", nullable=False)

    orden: Optional["Orden"] = Relationship(back_populates="productos")
    producto: Optional["Producto"] = Relationship(back_populates="ordenes")