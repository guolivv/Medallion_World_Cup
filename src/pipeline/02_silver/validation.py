import pandas as pd
import logging
import inspect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

player_csv_path = 'data/02_silver/df_players.csv'
goal_csv_path = 'data/02_silver/df_goals.csv'

df_goals = pd.read_csv(goal_csv_path)
df_players = pd.read_csv(player_csv_path)


def validation_name_goal_to_player(df_goals:pd.DataFrame, df_players:pd.DataFrame) -> pd.DataFrame:
    logging.info(f'Validação {inspect.currentframe().f_code.co_name} iniciada')

    names = df_goals.merge(
        df_players,
        on='name',
        how='left',
        indicator=True
    )

    problem_names = names[names['_merge'] == 'left_only']

    logging.info(f'Validação {inspect.currentframe().f_code.co_name} encontrou {problem_names.shape[0]} nomes para tratamento: \n {problem_names}')


validation_name_goal_to_player(df_goals, df_players)