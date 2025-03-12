import requests
import json
import time

'''def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None'''


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    


def request(api):
    retries=5
    backoff=2
    attempt = 0
    while attempt < retries:
        response = requests.get(api)       
        if response.status_code == 200:
            return response
        
        elif response.status_code == 429:
            wait_time = backoff * (2 ** attempt)  # Exponential backoff
            print(f"Retry {attempt + 1}: Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            attempt += 1
        
        else:
            print(f"Failed to fetch data from {api}. Status code: {response.status_code}")
            return None
    
    print("Max retries reached. Returning None.")
    return None