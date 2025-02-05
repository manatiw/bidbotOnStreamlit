import json
import pandas as pd
import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime
import pytz



new_tender_df = pd.DataFrame()
new_award_df = pd.DataFrame()


# search with title
for keyword in TITLE_KEYWORDS:
    print(keyword)

    title_search_df = search_api(keyword, API_BY_TITLE, START_DATE)
    tender_df, award_df = scrape_data(title_search_df)

    tender_df.insert(0, 'keyword', keyword)
    award_df.insert(0, 'keyword', keyword)
    new_tender_df = pd.concat([new_tender_df, tender_df], ignore_index=True)
    new_award_df = pd.concat([new_award_df, award_df], ignore_index=True)

new_tender_df = new_tender_df.rename(columns={'機關資料:機關名稱': '機關名稱'})



# search with company
for keyword in COMPANY_KEYWORDS:
    print(keyword)

    company_search_df = search_api(keyword, API_BY_COMPANY, START_DATE)
    tender_df, award_df = scrape_data(company_search_df)
    tender_df.insert(0, 'keyword', keyword)
    award_df.insert(0, 'keyword', keyword)
    new_tender_df = pd.concat([new_tender_df, tender_df], ignore_index=True)
    new_award_df = pd.concat([new_award_df, award_df], ignore_index=True)

    # Award table formatting
# Define the column pairs for combination
column_pairs = [
    ('機關名稱', '機關資料:機關名稱', '無法決標公告:機關名稱'),
    ('單位名稱', '機關資料:單位名稱', '無法決標公告:單位名稱'),
    ('聯絡人', '機關資料:聯絡人', '無法決標公告:聯絡人'),
    ('聯絡電話', '機關資料:聯絡電話', '無法決標公告:聯絡電話'),
    ('電子郵件信箱', '機關資料:電子郵件信箱', '無法決標公告:電子郵件信箱'),
    ('傳真號碼', '機關資料:傳真號碼', '無法決標公告:傳真號碼'),
    ('標的分類', '採購資料:標的分類', '無法決標公告:標的分類')
]

for new_col, col1, col2 in column_pairs:
    if col1 in new_award_df.columns and col2 in new_award_df.columns:
        new_award_df[new_col] = new_award_df[col1].combine_first(new_award_df[col2])
    elif col1 in new_award_df.columns:
        new_award_df[new_col] = new_award_df[col1]
    elif col2 in new_award_df.columns:
        new_award_df[new_col] = new_award_df[col2]

# Check for '已公告資料:標的分類' separately since it is only used in the last step
if '已公告資料:標的分類' in new_award_df.columns:
    new_award_df['標的分類'] = new_award_df['標的分類'].combine_first(new_award_df['已公告資料:標的分類'])

# Drop only the columns that exist in the DataFrame
columns_to_drop = ['機關資料:機關名稱', '無法決標公告:機關名稱', '機關資料:單位名稱', '無法決標公告:單位名稱',
                   '機關資料:聯絡人', '無法決標公告:聯絡人', '機關資料:聯絡電話', '無法決標公告:聯絡電話',
                   '機關資料:電子郵件信箱', '無法決標公告:電子郵件信箱', '機關資料:傳真號碼',
                   '無法決標公告:傳真號碼', '採購資料:標的分類', '已公告資料:標的分類', '無法決標公告:標的分類']

# Use set intersection to find only columns that exist in the DataFrame
existing_columns_to_drop = [col for col in columns_to_drop if col in new_award_df.columns]

# Drop the existing columns
new_award_df.drop(existing_columns_to_drop, axis=1, inplace=True)


# New tender標的分類
values_to_keep = ['財物類352-醫藥產品', '財物類481-醫療,外科及矯形設備', '財物類482-做為測量、檢查、航行及其他目的用之儀器和裝置，除光學儀器;工業程序控制設備;上述各項之零件及附件', '財物類483-光學儀器,攝影設備及其零件與附件', '財物類449-其他特殊用途之機具及其零件']

if '採購資料:標的分類' in new_tender_df.columns:
    new_tender_df = new_tender_df.drop(new_tender_df.index[~new_tender_df['採購資料:標的分類'].isin(values_to_keep)])