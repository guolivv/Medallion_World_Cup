from dotenv import load_dotenv
import os
import requests
import logging
import json
import pandas as pd
from requests.exceptions import Timeout, ConnectionError, HTTPError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_raw_data(urls:list) -> None:

    for url in urls:
        endpoint = list(url.keys())[0]

        logging.info(f'Endpoint {endpoint} | Extração iniciada')

        try:
            response = requests.get(list(url.values())[0])

            if response.raise_for_status():
                logging.error(f'Endpoint {endpoint} | Erro na requisição')
                return []

            data = response.json()

            if not data:
                logging.warning(f'Endpoint {endpoint} | Nenhum dado retornado')
                return []
            
            output_path = f'data/raw/{endpoint}.json'
            with open(output_path, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logging.info(f'Endpoint {endpoint} | Dados salvos em {output_path}')
            logging.info(f'Endpoint {endpoint} | Extração bem sucedida')


        except Timeout:
            logging.error(f'Endpoint {endpoint} | Erro: timeout')
        except ConnectionError:
            logging.error(f'Endpoint {endpoint} | Erro: ConnectionError')
        except HTTPError as erro_http:
            logging.error(f'Endpoint {endpoint} | Erro HTTP do servidor: {erro_http}')
        except Exception as erro_generico:
            logging.error(f'Endpoint {endpoint} | Erro inesperado: {erro_generico}')


if __name__ == '__main__':
    urls = [
            {'worldcup':'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'},
            # {'squads':'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.squads.json'},
            # {'groups':'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.groups.json'}
    ]

    extract_raw_data(urls)