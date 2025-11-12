from tkinter import NO
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from api.models import CreateProduct, ReadPago, ReadProduct
from db.session import DBSessionManager
from db.entities import Pago, Producto
from util.logger import LoggerSessionManager



class ProductoRouter:
    router = APIRouter(prefix="/productos", tags=["Productos"])

    def __init__(
        self, db_session_manager: DBSessionManager, logger_session_manager: LoggerSessionManager
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

class PagosRouter:
    router = APIRouter(prefix="/pagos", tags=["Pagos"])

    def __init__(self, db_session_manager: DBSessionManager, logger_session_manager: LoggerSessionManager):
        self.db_session_manager = db_session_manager
        self.logger_session = logger_session_manager
        self.logger = logger_session_manager.get_logger(__name__)

        @self.router.get(path="/{pago_id}", response_model=ReadPago)
        def get_pago_by_id(pago_id: int, request: Request):
            db_session: Session = request.state.db_session
            pago = db_session.query(Pago).where(Pago.id==pago_id).all()
            if len(pago)==0:
                raise HTTPException(status_code=404, detail="Not found")
            return pago[0]

