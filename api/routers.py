from pyclbr import Class
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from api.models import (
    CreateProduct,
    BaseReadOrder,
    ReadOrderWithUser,
    ReadProduct,
    BaseReadUser,
    ReadUserWithOrders,
)
from db.session import DBSessionManager, DBSessionMiddleware
from db.entities import Orden, Producto, Usuario
from util.logger import LoggerSessionManager


class ProductoRouter:
    router = APIRouter(prefix="/productos", tags=["Productos"])

    def __init__(
        self,
        db_session_manager: DBSessionManager,
        logger_session_manager: LoggerSessionManager,
    ):
        self.db_session_manager = db_session_manager
        self.logger_session = logger_session_manager
        self.logger = logger_session_manager.get_logger(__name__)

        self.router = APIRouter(prefix="/productos", tags=["Productos"])

        self.router.add_api_route(
            "/", self.list, methods=["GET"], response_model=list[ReadProduct]
        )
        self.router.add_api_route(
            "/{producto_id}", self.get, methods=["GET"], response_model=ReadProduct
        )
        self.router.add_api_route(
            "/", self.create, methods=["POST"], response_model=ReadProduct
        )
        self.router.add_api_route(
            "/{producto_id}",
            self.update,
            methods=["PUT"],
            response_model=ReadProduct,
        )
        self.router.add_api_route("/{producto_id}", self.delete, methods=["DELETE"])

    def list(self, request: Request):
        db_session: Session = request.state.db_session
        self.logger.info("Querying all products")
        return db_session.query(Producto).all()

    def get(self, producto_id: int, request: Request):
        db_session: Session = request.state.db_session
        self.logger.info(f"Getting product with id: {producto_id}")
        prod = db_session.query(Producto).get(producto_id)
        if not prod:
            return JSONResponse(
                status_code=404, content={"error_description": "Not found"}
            )
        return prod

    def create(self, data: CreateProduct, request: Request):
        db_session: Session = request.state.db_session
        new_product = Producto(**data.model_dump())
        db_session.add(new_product)
        db_session.flush()
        return new_product

    def update(self, producto_id: int, data: CreateProduct, request: Request):
        db_session: Session = request.state.db_session
        updated_product = db_session.query(Producto).get(producto_id)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in data.model_dump().items():
            setattr(updated_product, key, value)
        db_session.flush()
        return updated_product

    def delete(self, producto_id: int, request: Request):
        db_session: Session = request.state.db_session
        prod = db_session.query(Producto).get(producto_id)
        if not prod:
            raise HTTPException(status_code=404, detail="Not found")
        db_session.delete(prod)
        return {"message": "Product deleted"}


class UsuarioRouter:
    router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

    def __init__(
        self,
        db_session_manager: DBSessionManager,
        logger_session_manager: LoggerSessionManager,
    ):
        self.db_session_manager = db_session_manager
        self.logger_session = logger_session_manager
        self.logger = logger_session_manager.get_logger(__name__)

        @self.router.get("/{user_id}", response_model=ReadUserWithOrders)
        def get_user_by_id(
            user_id: int,
            db_session: Session = Depends(DBSessionMiddleware.get_db_session),
        ):
            # user = (
            #     db_session.query(Usuario, Orden)
            #     .join(Orden, Orden.usuario_id == Usuario.id, isouter=True)
            #     .where(Usuario.id == user_id)
            #     .all()
            # )
            user: Usuario = db_session.query(Usuario).get(user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="Not found")

            return user


class OrdenesRouter:
    router = APIRouter(prefix="/ordenes", tags=["Ordenes"])

    def __init__(
        self,
        db_session_manager: DBSessionManager,
        logger_session_manager: LoggerSessionManager,
    ):
        self.db_session_manager = db_session_manager
        self.logger_session = logger_session_manager
        self.logger = logger_session_manager.get_logger(__name__)

        @self.router.get("/{orden_id}", response_model=ReadOrderWithUser)
        def get_orden_by_id(
            orden_id: int,
            db_session: Session = Depends(DBSessionMiddleware.get_db_session),
        ):
            orden: Orden = db_session.query(Orden).get(orden_id)
            if orden is None:
                raise HTTPException(status_code=404, detail="Not found")
            return orden
