import json
import time
from copy import copy
from pathlib import Path
import requests


class Parser_5ka:
    # def __init__(self):
    #     self.api_url = "https://5ka.ru/api/v2"
    #     self.endpoint_so = '/special_offers'
    #     self.params = {"records_per_page": 100, "page": 1}
    #     self.headers = {
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
    #         'Accept': 'application/json',
    #     }

    def __init__(self):
        self.api_url = "https://5ka.ru/api/v2"
        self.endpoint_so = '/categories'
        self.params = {"records_per_page": 100, "page": 1}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept': 'application/json',
        }

    def parse(self):
        url = f'{self.api_url}{self.endpoint_so}'
        params = copy(self.params)
        while url:
            response = requests.get(url)

            if response.status_code >= 500:
                time.sleep(1)
                continue

            data = response.json()
            # url = data['next']
            params = {}

            for itm in data:
                self.save_categories(itm)
            time.sleep(1)


    def save_categories(self, data: dict):
        file_path = Path('data').joinpath(f"{data['parent_group_name']}.json")
        with open(file_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False)


    def parse_product(self):
        url = f'{self.api_url}{self.endpoint_so}'
        params = copy(self.params)
        while url:
            response = requests.get(url)

            if response.status_code >= 500:
                time.sleep(1)
                continue

            data = response.json()
            # url = data['next']
            params = {}

            for itm in data:
                self.save_categories(itm)
            time.sleep(1)

if __name__ == '__main__':
    parser = Parser_5ka()
    parser.parse()