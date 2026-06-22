import pandas as pd
import ast
import logging
import inspect
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def map_and_clean(row:pd.Series) -> Optional[list]:
    try:
        if pd.isna(row['score_ft']) and row['score_ft'] == '[0, 0]':
            print(row['date'])
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
    df_goals2 = df_goals2.rename(columns={'team1':'team', 'team2':'rival_team'})
    df_goals2['owngoal'] = df_goals2['owngoal'].fillna('False').astype('string')
    df_goals2['penalty'] = df_goals2['penalty'].fillna('False').astype('string')
    df_goals2.to_csv('data/02_silver/goals2.csv', index=False)
    


if __name__ == '__main__':
    worldcup_to_goals()