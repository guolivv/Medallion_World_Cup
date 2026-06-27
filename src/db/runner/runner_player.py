
import csv
from pathlib import Path
from src.db.config import DBConfig
from src.db.connection import db_session
from src.db.repository.repository_player import PlayerRepository
from dotenv import load_dotenv

load_dotenv()

config = DBConfig.from_env()
                     
CSV_PATH = Path(__file__).parent.parent.parent.parent  / "data" / "02_silver" / "df_players.csv"

linhas_inseridas_total = 0

with db_session(config) as conn:
    repo = PlayerRepository(conn)
    
    with open(CSV_PATH, mode="r", encoding="utf-8") as archive:
        csv_reader = csv.DictReader(archive)
        
        for line in csv_reader:
            data_player = {
                "number": line["number"],
                "pos": line["pos"],
                "name": line["name"],
                "date_of_birth": line["date_of_birth"],
                "club_name": line["club_name"],
                "club_country": line["club_country"],
                "confederation_name": line["confederation_name"],
                "fifa_code": line["fifa_code"]
            }
            
            sucesso = repo.insert(data_player)
            linhas_inseridas_total += sucesso

print(f"Sucesso! Total de linhas adicionadas: {linhas_inseridas_total}")