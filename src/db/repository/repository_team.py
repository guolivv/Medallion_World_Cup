from typing import Any
from psycopg2.extensions import connection as PgConnection
import logging

logger = logging.getLogger(__name__)

class TeamRepository:
    def __init__(self, conn: PgConnection):
        self.conn = conn

        
    def insert(self, team: dict[str, Any]) -> int:
        query = """
            INSERT INTO team (fifa_code, name, group_name)
            VALUES (%(fifa_code)s, %(name)s, %(group_name)s);
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, team)
            return cursor.rowcount