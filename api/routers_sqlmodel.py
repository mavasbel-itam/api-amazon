from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from db.session import DBSessionManager, DBSessionMiddleware
from db.entities_sqlmodel import Orden, Producto, Usuario, Pago

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

        self.router.add_api_route(
            "/", self.list, methods=["GET"], response_model=list[Producto]
        )
        self.router.add_api_route(
            "/{producto_id}", self.get, methods=["GET"], response_model=Producto
        )
        self.router.add_api_route(
            "/", self.create, methods=["POST"], response_model=Producto
        )
        self.router.add_api_route(
            "/{producto_id}",
            self.update,
            methods=["PUT"],
            response_model=Producto,
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

    def create(self, data: Producto, request: Request):
        db_session: Session = request.state.db_session
        new_product = Producto(**data.model_dump())
        db_session.add(new_product)
        db_session.flush()
        return new_product

    def update(self, producto_id: int, data: Producto, request: Request):
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
        @self.router.get("/{user_id}", response_model=Usuario)
        def get_user_by_id(
            user_id: int,
            db_session: Session = Depends(DBSessionMiddleware.get_db_session),
        ):
            user: Usuario = db_session.query(Usuario).get(user_id)
            if user is None:
                raise HTTPException(status_code=404, detail="Not found")
            return user


class PagosRouter:
    router = APIRouter(prefix="/pagos", tags=["Pagos"])

    def __init__(
        self,
        db_session_manager: DBSessionManager,
        logger_session_manager: LoggerSessionManager,
    ):
        self.db_session_manager = db_session_manager
        self.logger_session = logger_session_manager
        self.logger = logger_session_manager.get_logger(__name__)

        @self.router.get(path="/{pago_id}", response_model=Pago)
        def get_pago_by_id(pago_id: int, request: Request):
            db_session: Session = request.state.db_session
            pago = db_session.query(Pago).where(Pago.id == pago_id).all()
            if len(pago) == 0:
                raise HTTPException(status_code=404, detail="Not found")
            return pago[0]


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

        @self.router.get("/{orden_id}", response_model=Orden)
        def get_orden_by_id(
            orden_id: int,
            db_session: Session = Depends(DBSessionMiddleware.get_db_session),
        ):
            orden: Orden = db_session.query(Orden).get(orden_id)
            if orden is None:
                raise HTTPException(status_code=404, detail="Not found")
            return orden