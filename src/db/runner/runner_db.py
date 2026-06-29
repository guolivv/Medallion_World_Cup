import logging
import os
from pathlib import Path
from psycopg2.extensions import connection as PgConnection

logger = logging.getLogger(__name__)

DDL_DIR = Path(__file__).parent.parent / "ddl"

def run_migrations(conn: PgConnection) -> None:
    extensions = ['.sql', '.sh']
    sql_sh_files = sorted(f for f in DDL_DIR.glob("*") if f.suffix.lower() in extensions)
    print(sql_sh_files)

    try:
        with conn.cursor() as cur:
            for sql_file in sql_sh_files:
                logger.info(f"Aplicando schema: {sql_file.name}")
                sql_content = sql_file.read_text()
                sql_content = sql_content.format(
                    READONLY_PASSWORD=os.environ["READONLY_PASSWORD"],
                    POSTGRES_DB=os.environ["POSTGRES_DB"],
                )
                cur.execute(sql_content)

        conn.commit()
        logger.info(f"{len(sql_sh_files)} arquivo(s) de schema aplicado(s) com sucesso.")
    except Exception as e:
        print(f'Exceção: {e}')
        conn.rollback()
        raise