from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)

    productos: Mapped[list["ProductoCategoria"]] = relationship(
        "ProductoCategoria", back_populates="categoria", cascade="all, delete-orphan"
    )


class Producto(Base):
    __tablename__ = "producto"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    imagen: Mapped[str] = mapped_column(String(100), nullable=False)

    categorias: Mapped[list["ProductoCategoria"]] = relationship(
        "ProductoCategoria", back_populates="producto", cascade="all, delete-orphan"
    )

class ProductoCategoria(Base):
    __tablename__ = "producto_categoria"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
    )
    producto_id: Mapped[int] = mapped_column(
        ForeignKey("producto.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
    )

    categoria: Mapped["Categoria"] = relationship(
        "Categoria", back_populates="productos"
    )
    producto: Mapped["Producto"] = relationship("Producto", back_populates="categorias")
