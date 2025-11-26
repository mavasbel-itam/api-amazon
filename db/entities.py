from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    BigInteger,
    Numeric,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ------------------------------
# Categoria
# ------------------------------
class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(300), nullable=False, unique=True)

    productos = relationship(
        "ProductoCategoria", back_populates="categoria", cascade="all, delete-orphan"
    )


# ------------------------------
# Producto
# ------------------------------
class Producto(Base):
    __tablename__ = "producto"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(300), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(Numeric(12, 2), nullable=False)
    imagen = Column(String(100), nullable=False)

    categorias = relationship(
        "ProductoCategoria", back_populates="producto", cascade="all, delete-orphan"
    )

    ordenes = relationship(
        "ProductoOrden", back_populates="producto", cascade="all, delete-orphan"
    )


# ------------------------------
# Usuario
# ------------------------------
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(300), nullable=False)
    apellido = Column(String(300), nullable=False)
    telefono = Column(String(15), nullable=False, unique=True)
    correo = Column(String(254), nullable=False, unique=True)
    contrasena = Column(String(100), nullable=False)
    es_prime = Column(Boolean, nullable=False)

    ordenes = relationship("Orden", back_populates="usuario")


# ------------------------------
# Orden
# ------------------------------
class Orden(Base):
    __tablename__ = "orden"

    id = Column(BigInteger, primary_key=True)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False)
    fecha_entrega = Column(DateTime(timezone=True))
    direccion_entrega = Column(Text, nullable=False)

    usuario_id = Column(
        BigInteger,
        ForeignKey("usuario.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
    )

    usuario = relationship("Usuario", back_populates="ordenes")
    pagos = relationship("Pago", back_populates="orden")
    productos = relationship("ProductoOrden", back_populates="orden")


# ------------------------------
# Pago
# ------------------------------
class Pago(Base):
    __tablename__ = "pago"

    id = Column(BigInteger, primary_key=True)
    fecha_pago = Column(DateTime(timezone=True), nullable=False)
    fecha_validacion = Column(DateTime(timezone=True))
    monto = Column(Numeric(12, 2), nullable=False)
    validado = Column(Boolean, nullable=False)

    orden_id = Column(
        BigInteger,
        ForeignKey("orden.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
    )

    orden = relationship("Orden", back_populates="pagos")


# ------------------------------
# ProductoCategoria (Association Object)
# ------------------------------
class ProductoCategoria(Base):
    __tablename__ = "producto_categoria"

    id = Column(BigInteger, primary_key=True)

    categoria_id = Column(
        BigInteger,
        ForeignKey("categoria.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
    )
    producto_id = Column(
        BigInteger,
        ForeignKey("producto.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False,
    )

    categoria = relationship("Categoria", back_populates="productos")
    producto = relationship("Producto", back_populates="categorias")


# ------------------------------
# ProductoOrden (Association Object)
# ------------------------------
class ProductoOrden(Base):
    __tablename__ = "producto_orden"

    id = Column(BigInteger, primary_key=True)
    cantidad = Column(Integer, nullable=False)

    orden_id = Column(
        BigInteger,
        ForeignKey("orden.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
    )
    producto_id = Column(
        BigInteger,
        ForeignKey("producto.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
    )

    orden = relationship("Orden", back_populates="productos")
    producto = relationship("Producto", back_populates="ordenes")
