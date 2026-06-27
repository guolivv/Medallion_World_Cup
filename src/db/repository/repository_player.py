from typing import Any
from psycopg2.extensions import connection as PgConnection
import logging

logger = logging.getLogger(__name__)

class PlayerRepository:
    def __init__(self, conn: PgConnection):
        self.conn = conn


    def insert(self, player: dict[str, Any]) -> int:
        query = """
            INSERT INTO player (number, pos, name, date_of_birth, club_name, club_country, confederation_name, fifa_code)
            VALUES (%(number)s, %(pos)s, %(name)s, %(date_of_birth)s, %(club_name)s, %(club_country)s, %(confederation_name)s, %(fifa_code)s);
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, player)
            return cursor.rowcount