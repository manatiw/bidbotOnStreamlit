import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")



with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

# Keywords
TITLE_KEYWORDS = config['keywords']['by_title']
COMPANY_KEYWORDS = config['keywords']['by_company']

# Search Methods, might delete
API_BASE_URL = config['websites']['g0v']['api']['base_url']
API_BY_TITLE = config['websites']['g0v']['api']['endpoints']['search_title']
API_BY_COMPANY = config['websites']['g0v']['api']['endpoints']['search_company']

# Record Methods
TENDER_SELECTED_COLUMNS = config["data_to_collect"]["pcc_gov"]["tender_columns"]
AWARD_SELECTED_COLUMNS = config["data_to_collect"]["pcc_gov"]["award_columns"]
NOT_AWARD_SELECTED_COLUMNS = config["data_to_collect"]["pcc_gov"]["not_award_columns"]
