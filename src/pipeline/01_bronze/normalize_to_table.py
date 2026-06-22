import pandas as pd
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def normalize_static() -> None:
    logging.info('Static | Normalização iniciada')

    input_dir = 'data/raw/'

    for file in os.listdir(input_dir):
        name, ext = os.path.splitext(file)
        input_path_json = os.path.join(input_dir, file)
        
        if name == 'groups':
            with open(input_path_json, 'r', encoding='utf-8') as f:
                data_json = json.load(f)
            
            data_json['tournament_name'] = data_json.pop('name')
            df_groups = pd.json_normalize(data_json, record_path='groups', meta='tournament_name')
            output_path_csv = 'data/01_bronze/df_groups.csv'
            df_groups.to_csv(output_path_csv)

            logging.info(f'Static groups | Dados salvos em {output_path_csv}')
            logging.info('Static groups | Normalização bem sucedida')

        if name == 'squads':
            with open(input_path_json, 'r', encoding='utf-8') as f:
                data_json = json.load(f)

            df_squads = pd.json_normalize(data_json)
            output_path_csv = 'data/01_bronze/df_squads.csv'
            df_squads.to_csv('data/01_bronze/df_squads.csv')

            logging.info(f'Static squads | Dados salvos em {output_path_csv}')
            logging.info('Static squads | Normalização bem sucedida')


def normalize_dynamic() -> None:
    logging.info('Dynamic | Normalização iniciada')

    input_path_json = 'data/raw/worldcup.json'

    with open(input_path_json, 'r', encoding='utf-8') as f:
        data_json = json.load(f)

    df_worldcup = pd.json_normalize(data_json, record_path='matches')
    df_worldcup = df_worldcup.drop(columns='num')
    df_worldcup = df_worldcup.rename(columns={'score.ft':'score_ft','score.ht':'score_ht'})

    output_path_csv = 'data/01_bronze/df_worldcup.csv'
    df_worldcup.to_csv(output_path_csv)

    logging.info(f'Dynamic worldcup | Dados salvos em {output_path_csv}')
    logging.info('Dynamic worldcup | Normalização bem sucedida')


if __name__ == '__main__':
    # normalize_static()
    normalize_dynamic()