from fastapi import FastAPI
from db.entities import Base
from db.session import DBSessionManager, DBSessionMiddleware
from api.routers import ProductoRouter
from util.logger import LoggerSessionManager

logger_session_manager = LoggerSessionManager()

db_session_manager = DBSessionManager(logger_session_manager)
Base.metadata.create_all(bind=db_session_manager.engine)

producto_router = ProductoRouter(db_session_manager, logger_session_manager)

app = FastAPI(title="API CRUD (FastAPI + SQLAlchemy)")
app.include_router(producto_router.router)
app.add_middleware(DBSessionMiddleware, db_session_manager=db_session_manager)
