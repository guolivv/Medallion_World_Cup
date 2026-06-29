import pandas as pd
import ast
import logging
import inspect
from typing import Optional
import unicodedata

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def map_and_clean(row:pd.Series) -> Optional[list]:
    try:
        if pd.isna(row['score_ft']) and row['score_ft'] == '[0, 0]':
            return pd.Series([g1, g2], index=['goals1', 'goals2'])
        else:
            g1 = row['goals1']
            g2 = row['goals2']

            if isinstance(g1, str) and isinstance(g2, str):
                g1_eval = ast.literal_eval(g1)
                g2_eval = ast.literal_eval(g2)

                return pd.Series([g1_eval, g2_eval], index=['goals1', 'goals2'])
    except Exception as erro:
        print(f'Exceção: O valor g1: {g1} ou g2: {g2} gerou o erro {erro}') 
        return None
    

def minute_converter(text:str) -> int:
    if isinstance(text, str) and '+' in text:
        partes = text.split('+')
        return int(partes[0]) + int(partes[1])
    
    return int(text)


def remove_accents(text:str) -> str:
    if isinstance(text, str):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text 


def change_columns(df:pd.DataFrame) -> pd.DataFrame:
    df['team'] = df['team2']
    df['rival_team'] = df['team1']
    df.drop(columns=['team1', 'team2'], inplace=True)
    return df


def map_diff(df:pd.DataFrame) -> pd.DataFrame:
    # teams
    df['team'] = df['team'].str.replace('usa', 'united states')
    df['rival_team'] = df['rival_team'].str.replace('usa', 'united states')

    # players
    dict_players = {
        'mahmoud abunada':'mahmud abunada',
        'baris alper yilmaz':'barıs alper yılmaz',
        'mohammad mohebbi':'mohammad mohebi',
        'maxi araujo':'maximiliano araujo',
        'agustin cano':'agustin canobbio',
        'mostafa zico':'mostafa ziko',
        'mousa al-tamari':'musa al-taamari',
        'stephan eustaquio':'stephen eustaquio'
    }

    df['name'] = df['name'].replace(dict_players)

    return df


def worldcup_to_goals():
    input_path = 'data/01_bronze/df_worldcup.csv'

    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} iniciada')

    df_worldcup = pd.read_csv(input_path)
    df_worldcup[['goals1', 'goals2']] = df_worldcup.apply(map_and_clean, axis=1)
    df_worldcup = df_worldcup.drop(columns='Unnamed: 0')
    df_worldcup['goals1'] = df_worldcup['goals1'].replace('"', '')
    df_worldcup['goals2'] = df_worldcup['goals2'].replace('"', '')

    df_goals1 = pd.json_normalize(df_worldcup.to_dict(orient='records'), record_path='goals1', meta=['team1', 'team2', 'ground'])
    df_goals1 = df_goals1.rename(columns={'team1':'team', 'team2':'rival_team'})
    df_goals1['owngoal'] = df_goals1['owngoal'].fillna('False').astype('string')
    df_goals1['penalty'] = df_goals1['penalty'].fillna('False').astype('string')
    df_goals1.to_csv('data/02_silver/goals1.csv', index=False)

    df_goals2 = pd.json_normalize(df_worldcup.to_dict(orient='records'), record_path='goals2', meta=['team1', 'team2', 'ground'])
    change_columns(df_goals2)
    df_goals2['owngoal'] = df_goals2['owngoal'].fillna('False').astype('string')
    df_goals2['penalty'] = df_goals2['penalty'].fillna('False').astype('string')
    df_goals2.to_csv('data/02_silver/goals2.csv', index=False)

    df_goals = pd.concat([df_goals1, df_goals2], ignore_index=True)
    df_goals['name'] = df_goals['name'].str.lower()
    df_goals['team'] = df_goals['team'].str.lower()
    df_goals['team'] = df_goals['team'].str.replace('&', 'and')
    df_goals['rival_team'] = df_goals['rival_team'].str.lower()
    df_goals['rival_team'] = df_goals['rival_team'].str.replace('&', 'and')
    df_goals['minute'] = df_goals['minute'].apply(minute_converter)
    df_goals['name'] = df_goals['name'].apply(remove_accents)
    map_diff(df_goals)

    df_goals.to_csv('data/02_silver/df_goals.csv', index=False)
    logging.info(f'Transformação {inspect.currentframe().f_code.co_name} finalizada!')


if __name__ == '__main__':
    worldcup_to_goals()