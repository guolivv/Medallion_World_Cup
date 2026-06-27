from src.db.config import DBConfig
from src.db.connection import get_connection
from src.db.runner.runner_db import run_migrations
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

config = DBConfig.from_env()
conn = get_connection(config)

try:
    run_migrations(conn)
finally:
    conn.close()