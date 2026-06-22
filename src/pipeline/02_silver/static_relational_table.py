import pandas as pd
import ast
import logging
import inspect
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def map_and_clean(texto:str) -> Optional[list]:
    try:
        return ast.literal_eval(texto)
    except Exception as erro:
        print(f'Exceção: {erro}') 
        return None       


def squads_to_players() -> None:
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} iniciada')

    input_path = 'data/01_bronze/df_squads.csv'
    df_squads = pd.read_csv(input_path)
    df_squads['players'] = df_squads['players'].str.replace('""', '"')
    df_squads['players'] = df_squads['players'].apply(map_and_clean)
    df_squads['confederation_name'] = df_squads.pop('name')

    df_players = pd.json_normalize(df_squads.to_dict(orient='records'), record_path='players', meta=['confederation_name', 'fifa_code', 'group'])
    df_players = df_players.rename(columns={'club.name':'club_name', 'club.country':'club_country'})
    df_players.to_csv('data/02_silver/df_players.csv', index=False)


def squads_to_teams() -> None:
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} iniciada')

    input_path = 'data/01_bronze/df_squads.csv'
    df_squads = pd.read_csv(input_path)
    df_teams = df_squads.drop(columns=['players', 'Unnamed: 0'])
    df_teams.to_csv('data/02_silver/df_teams.csv', index=False)


if __name__ == '__main__':
    squads_to_players()
    squads_to_teams()