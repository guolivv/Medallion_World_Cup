import pandas as pd
import ast
import logging
import inspect
from typing import Optional
import unicodedata

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def map_and_clean(texto:str) -> Optional[list]:
    try:
        return ast.literal_eval(texto)
    except Exception as erro:
        print(f'Exceção: {erro}') 
        return None  


def remove_accents(text:str) -> str:
    if isinstance(text, str):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text     


def to_lower(text:str) -> str:
    return text.lower()


def rename_columns(df:pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        'club.name':'club_name',
        'club.country':'club_country',
        'group':'group_name'
    }, inplace=True)                     


def squads_to_players() -> None:
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} iniciada')

    input_path = 'data/01_bronze/df_squads.csv'
    df_squads = pd.read_csv(input_path)
    df_squads['players'] = df_squads['players'].str.replace('""', '"')
    df_squads['players'] = df_squads['players'].apply(map_and_clean)
    df_squads['confederation_name'] = df_squads.pop('name')

    df_players = pd.json_normalize(df_squads.to_dict(orient='records'), record_path='players', meta=['confederation_name', 'fifa_code'])
    df_players['name'] = df_players['name'].apply(to_lower)
    df_players['name'] = df_players['name'].apply(remove_accents)
    df_players['confederation_name'] = df_players['confederation_name'].apply(to_lower)         
    rename_columns(df_players)

    df_players.to_csv('data/02_silver/df_players.csv', index=False)
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} finalizada!')


def squads_to_teams() -> None:
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} iniciada')

    input_path = 'data/01_bronze/df_squads.csv'
    df_squads = pd.read_csv(input_path)
    df_teams = df_squads.drop(columns=['players', 'Unnamed: 0'])
    df_teams['name'] = df_teams['name'].apply(to_lower)
    rename_columns(df_teams)
    
    df_teams.to_csv('data/02_silver/df_teams.csv', index=False)
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} finalizada!')


if __name__ == '__main__':
    squads_to_players()
    squads_to_teams()