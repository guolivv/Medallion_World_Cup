import logging
from pathlib import Path
from psycopg2.extensions import connection as PgConnection

logger = logging.getLogger(__name__)

DDL_DIR = Path(__file__).parent.parent / "ddl"
 
def run_migrations(conn: PgConnection) -> None:
    sql_files = sorted(DDL_DIR.glob("*.sql"))

    try:
        with conn.cursor() as cur:
            for sql_file in sql_files:
                logger.info(f"Aplicando schema: {sql_file.name}")
                cur.execute(sql_file.read_text())

        conn.commit()
        logger.info(f"{len(sql_files)} arquivo(s) de schema aplicado(s) com sucesso.")
    except Exception as e:
        print(f'Exceção: {e}')
