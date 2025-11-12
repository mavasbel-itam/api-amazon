from datetime import datetime
from enum import auto
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    null,
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


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    apellido: Mapped[str] = mapped_column(String(300), nullable=False)
    telefono: Mapped[str] = mapped_column(String(15), nullable=False)
    correo: Mapped[str] = mapped_column(String(254), nullable=False)
    contrasena: Mapped[str] = mapped_column(String(100), nullable=False)
    es_prime: Mapped[bool] = mapped_column(Boolean, nullable=False)

    ordenes: Mapped[list["Orden"]] = relationship("Orden", back_populates="usuario")


class Orden(Base):
    __tablename__ = "orden"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    fecha_entrega: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    direccion_entrega: Mapped[str] = mapped_column(Text, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    usuario: Mapped[Usuario] = relationship("Usuario", back_populates="ordenes")
