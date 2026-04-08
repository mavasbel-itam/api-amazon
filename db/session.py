import os
from typing import Any, Dict, Tuple
from fastapi import Request, Response
from sqlalchemy import ClauseElement, Compiled, create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from db.entities_sqlalchemy import Base
from util.logger import LoggerSessionManager
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

# Read connection details from environment variables, falling back to defaults
DB_USER = os.environ.get("DATABASE_USER", "db_username")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD", "db_password")
DB_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_NAME = os.environ.get("DATABASE_NAME", "db_name")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class DBSessionManager:

    def __init__(
        self,
        logger_session_manager: LoggerSessionManager,
        db_url: str = DATABASE_URL,
        echo: bool = False,
    ):

        # Uncomment to see the DB schema generated from entities
        # logger = logger_session_manager.get_logger(__name__)
        # def executor(
        #     sql: ClauseElement | Compiled,
        #     *multiparams: Tuple[Any, ...],
        #     **params: Dict[str, Any],
        # ):
        #     logger.info(sql.compile(dialect=self.engine.dialect))
        # self.engine = create_engine(db_url, strategy="mock", executor=executor)
        # Base.metadata.create_all(bind=self.engine)

        self.engine = create_engine(db_url, echo=echo, future=True)
        self.logger_session_manager = logger_session_manager
        self.logger = self.logger_session_manager.get_logger()
        self.SessionLocal = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, future=True
        )

    @contextmanager
    def get_managed_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class DBSessionMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, db_session_manager: DBSessionManager):
        super().__init__(app)
        self.db_session_manager = db_session_manager

    async def dispatch(self, request: Request, call_next):
        with self.db_session_manager.get_managed_session() as db_session:
            request.state.db_session = db_session
            response: Response = await call_next(request)
            return response

    @staticmethod
    def get_db_session(request: Request) -> Session:
        return request.state.db_session
