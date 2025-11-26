from fastapi import FastAPI
from db.session import DBSessionManager, DBSessionMiddleware
from api.routers import OrdenesRouter, ProductoRouter, UsuarioRouter, PagosRouter
from util.logger import LoggerSessionManager

logger_session_manager = LoggerSessionManager()

db_session_manager = DBSessionManager(logger_session_manager)

producto_router = ProductoRouter(db_session_manager, logger_session_manager)
usuarios_router = UsuarioRouter(db_session_manager, logger_session_manager)
orden_router = OrdenesRouter(db_session_manager, logger_session_manager)
pagos_router = PagosRouter(db_session_manager, logger_session_manager)

app = FastAPI(title="API CRUD (FastAPI + Pydantic + SQLAlchemy)")
app.add_middleware(DBSessionMiddleware, db_session_manager=db_session_manager)
app.include_router(producto_router.router)
app.include_router(usuarios_router.router)
app.include_router(orden_router.router)
app.include_router(pagos_router.router)
