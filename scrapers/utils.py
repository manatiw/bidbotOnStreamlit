import requests
import json

def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)