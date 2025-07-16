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




class BrowserResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


def request(api):
    retries = 5
    backoff = 2
    attempt = 0

    while attempt < retries:
        try:
            return _browser_fetch(api)
        except Exception as e:
            wait_time = backoff * (2 ** attempt)
            print(f"Retry {attempt + 1} failed for {api}: {e}")
            time.sleep(wait_time)
            attempt += 1

    print("Max retries reached. Returning empty response.")
    return BrowserResponse({"records": []})


def _browser_fetch(api_url):
    async def _fetch():
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(api_url, timeout=60000)
                await page.wait_for_timeout(2000)

                raw_text = await page.inner_text("pre, body")
                if not raw_text.strip():
                    print(f"⚠️ Empty response at {api_url}")
                    return BrowserResponse({"records": []})

                json_data = json.loads(raw_text)
                return BrowserResponse(json_data)

            except Exception as e:
                print(f"❌ Error during browser fetch for {api_url}: {e}")
                return BrowserResponse({"records": []})

    return asyncio.run(_fetch())



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
