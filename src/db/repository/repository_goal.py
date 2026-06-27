from typing import Any
from psycopg2.extensions import connection as PgConnection
import logging

logger = logging.getLogger(__name__)

class GoalRepository:
    def __init__(self, conn: PgConnection):
        self.conn = conn

    def insert(self, goal: dict[str, Any]) -> int:
        query = """
            INSERT INTO goal (name, minute, owngoal, penalty, team_name, rival_team_name, ground)
            VALUES (%(name)s, %(minute)s, %(owngoal)s, %(penalty)s, %(team_name)s, %(rival_team_name)s, %(ground)s);
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, goal)
            return cursor.rowcount