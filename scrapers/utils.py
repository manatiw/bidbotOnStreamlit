import requests
import json
import time

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright


# old version do not use
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



class BrowserResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


async def request(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Fetching from: {url}")
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        # Some APIs return JSON directly in the <pre> or <body>
        raw_text = await page.inner_text("pre, body")

        try:
            data = json.loads(raw_text)
            print("✅ Successfully parsed JSON!")
            print("First few keys:", list(data.keys()) if isinstance(data, dict) else "Not a dict")
            return BrowserResponse(data)
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON:", str(e))
            print("Raw response snippet:\n", raw_text[:500])
            return None


'''def request(api):
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
    return None'''
