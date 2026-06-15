from dotenv import load_dotenv
import os
import requests
import logging
import json
import pandas as pd
from requests.exceptions import Timeout, ConnectionError, HTTPError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_raw_data(url:str) -> list:
    logging.info('Extração iniciada')

    try:
        response = requests.get(url)

        if response.raise_for_status():
            logging.error('Erro na requisição')
            return []

        data = response.json()

        if not data:
           logging.warning('Nenhum dado retornado')
           return []
        
        output_path = 'data/raw/worldcup_2026.json'
        with open(output_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logging.info('Extração bem sucedida!')
        return data


    except Timeout:
        logging.error('Erro: timeout')
    except ConnectionError:
        logging.error('Erro: ConnectionError')
    except HTTPError as erro_http:
        logging.error(f'Erro HTTP do servidor: {erro_http}')
    except Exception as erro_generico:
        logging.error(f'Erro inesperado: {erro_generico}')

    print(response.status_code)
    print(data.keys())


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'
    data = extract_raw_data(url)