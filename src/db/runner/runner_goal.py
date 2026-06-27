
import csv
from pathlib import Path
from src.db.config import DBConfig
from src.db.connection import db_session
from src.db.repository.repository_goal import GoalRepository
from dotenv import load_dotenv

load_dotenv()

config = DBConfig.from_env()
                     
CSV_PATH = Path(__file__).parent.parent.parent.parent  / "data" / "02_silver" / "df_goals.csv"

linhas_inseridas_total = 0

with db_session(config) as conn:
    repo = GoalRepository(conn)
    
    with open(CSV_PATH, mode="r", encoding="utf-8") as archive:
        csv_reader = csv.DictReader(archive)
        
        for line in csv_reader:
            data_goal = {
                "name": line["name"],
                "minute": line["minute"],
                "owngoal": line["owngoal"],
                "penalty": line["penalty"],
                "team_name": line["team"],
                "rival_team_name": line["rival_team"],
                "ground": line["ground"]
            }
            
            sucesso = repo.insert(data_goal)
            linhas_inseridas_total += sucesso

print(f"Sucesso! Total de linhas adicionadas: {linhas_inseridas_total}")