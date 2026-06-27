import logging
from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2.extensions import connection as PgConnection
from src.db.config import DBConfig

logger = logging.getLogger(__name__)

def get_connection(config: DBConfig) -> PgConnection:
    return psycopg2.connect(
        host=config.host,
        port=config.port,
        dbname=config.dbname,
        user=config.user,
        password=config.password,
    )


@contextmanager
def db_session(config: DBConfig) -> Generator[PgConnection, None, None]:
    conn = get_connection(config)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("Erro na transação, rollback executado.")
        raise
    finally:
        conn.close()