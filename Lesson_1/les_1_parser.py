import json
import time
from copy import copy
from pathlib import Path
import requests


class Parse5ka:
    def __init__(self):
        self.api_url = "https://5ka.ru/api/v2"
        self.endpoint_so = '/special_offers'
        self.params = {"records_per_page": 100, "page": 1}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept': 'application/json',
        }

    def parse(self):
        url = f'{self.api_url}{self.endpoint_so}'
        params = copy(self.params)
        while url:
            response = requests.get(url, params=params, headers=self.headers)

            if response.status_code >= 500:
                time.sleep(10)
                continue

            data = response.json()
            url = data['next']
            params = {}

            for itm in data['results']:
                self.save_to_file(itm)
            time.sleep(1)

    def save_to_file(self, data: dict):
        file_path = Path('data').joinpath(f"{data['id']}.json")
        with open(file_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = Parse5ka()
    parser.parse()