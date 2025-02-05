import json
import pandas as pd
import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


gov_search_df = pd.DataFrame()
baseUrl = "https://web.pcc.gov.tw/prkms/tender/common/bulletion/readBulletion"
href_baseUrl = 'https://web.pcc.gov.tw/'





#move to module
def request_html(api):
    response = requests.get(api)
    if response.status_code == 200:
        html_data = response.text
        return html_data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


gov_tender=pd.DataFrame()
gov_award=pd.DataFrame()


for keyword in TITLE_KEYWORDS:
  print(keyword)

  # Tender search result
  tenderQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%8B%9B%E6%A8%99&sortCol=TENDER_NOTICE_DATE&timeRange=" + str(minguoSearchYear) + "&pageSize=100"

  while True:
    html = request_html(baseUrl + tenderQueryStrings)
    soup = BeautifulSoup(html, 'html')
    tbody = soup.find("tbody")

    # extract data
    pattern = r'Geps3\.CNS\.pageCode2Img\("([^"]*)"\)'
    tender_names = re.findall(pattern, html)


    organizations = []
    job_numbers = []
    hyperlinks = []
    tender_dates = []
    award_dates = []
    tds = tbody.find_all("td")
    i = 0
    for td in tds:
      if i % 10 == 2:
        org = td.get_text(strip=True)
        organizations.append(org)
      elif i % 10 == 3:
        href = td.find('a')
        hyperlink = href['href']
        href = href_baseUrl + hyperlink
        hyperlinks.append(href)
        job_num = td.get_text(strip=True)
        job_numbers.append(job_num)
      elif i % 10 == 4:
        date = td.get_text(strip=True)
        roc_year, month, day = date.split('/')
        ce_year = str(int(roc_year) + 1911)
        formatted_date = ce_year + month + day
        tender_dates.append(formatted_date)
      elif i % 10 == 6:
        date = td.get_text(strip=True)
        award_dates.append(date)
      i += 1

    raw_gov_tender = pd.DataFrame({'date' : tender_dates, 'title' : tender_names,
                                  'keyword' : keyword, 'job_number' : job_numbers, '機關名稱' : organizations, '領投開標:截止投標': award_dates, 'url': hyperlinks} )

    raw_gov_tender['date'] = raw_gov_tender['date'].astype(int)
    df1 = raw_gov_tender[raw_gov_tender['date'] >= START_DATE]
    gov_tender = pd.concat([gov_tender,df1],ignore_index=True)

    break


    '''row_count = len(df1)
    if row_count < 100:
      break

    else:
      # Find the 'a' element with text "下一頁"
      next_page_link = soup.find('a', string='下一頁')
      # Extract the 'href' attribute
      if next_page_link is not None:
        tenderQueryStrings = next_page_link.get('href')
      else:
        print("next page not found")'''




  # Award search result
  awardQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%B1%BA%E6%A8%99&sortCol=AWARD_NOTICE_DATE&timeRange=" + str(minguoSearchYear) + "&pageSize=100"
  html = request_html(baseUrl + awardQueryStrings)
  soup = BeautifulSoup(html, 'html')
  tbody = soup.find("tbody")

  # extract data
  pattern = r'Geps3\.CNS\.pageCode2Img\("([^"]*)"\)'
  award_names = re.findall(pattern, html)

  organizations = []
  job_numbers = []
  hyperlinks = []
  award_dates = []
  award_types = []
  tds = tbody.find_all("td")
  i = 0
  for td in tds:
    if i % 10 == 2:
      org = td.get_text(strip=True)
      organizations.append(org)
    elif i % 10 == 3:
      href = td.find('a')
      hyperlink = href['href']
      href = href_baseUrl + hyperlink
      hyperlinks.append(href)
      job_num = td.get_text(strip=True)
      job_numbers.append(job_num)
    elif i % 10 == 5:
      td_date = td.get_text(strip=True)
      date = re.search(r'\d+/\d+/\d+', td_date).group()
      roc_year, month, day = date.split('/')
      ce_year = str(int(roc_year) + 1911)
      formatted_date = ce_year + month + day
      award_dates.append(formatted_date)
      award_given = td.find('span')
      if award_given:
        award_type = '無法決標公告'
      else:
        award_type = '決標公告'
      award_types.append(award_type)
    i += 1

  raw_gov_award = pd.DataFrame({'date' : award_dates, 'title' : award_names,
                                 'keyword' : keyword, 'type' : award_types, 'job_number' : job_numbers, '機關名稱' : organizations, 'url': hyperlinks} )
  raw_gov_award['date'] = raw_gov_award['date'].astype(int)
  df2 = raw_gov_award[raw_gov_award['date'] >= START_DATE]
  gov_award = pd.concat([gov_award,df2],ignore_index=True)



# Company keyword
for keyword in COMPANY_KEYWORDS:
  print(keyword)
  awardQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%B1%BA%E6%A8%99&sortCol=AWARD_NOTICE_DATE&timeRange=" + str(minguoSearchYear) + "&pageSize=100"

  html = request_html(baseUrl + awardQueryStrings)
  soup = BeautifulSoup(html, 'html')
  tbody = soup.find("tbody")

  # extract data
  pattern = r'Geps3\.CNS\.pageCode2Img\("([^"]*)"\)'
  award_names = re.findall(pattern, html)

  organizations = []
  job_numbers = []
  hyperlinks = []
  award_dates = []
  award_types = []
  tds = tbody.find_all("td")
  i = 0
  for td in tds:
    if i % 10 == 2:
      org = td.get_text(strip=True)
      organizations.append(org)
    elif i % 10 == 3:
      href = td.find('a')
      hyperlink = href['href']
      href = href_baseUrl + hyperlink
      hyperlinks.append(href)
      job_num = td.get_text(strip=True)
      job_numbers.append(job_num)
    elif i % 10 == 5:
      td_date = td.get_text(strip=True)
      date = re.search(r'\d+/\d+/\d+', td_date).group()
      roc_year, month, day = date.split('/')
      ce_year = str(int(roc_year) + 1911)
      formatted_date = ce_year + month + day
      award_dates.append(formatted_date)
      award_given = td.find('span')
      if award_given:
        award_type = '無法決標公告'
      else:
        award_type = '決標公告'
      award_types.append(award_type)
    i += 1

  raw_gov_award = pd.DataFrame({'date' : award_dates, 'title' : award_names,
                                 'keyword' : keyword, 'type' : award_types, 'job_number' : job_numbers, '機關名稱' : organizations, 'url': hyperlinks} )
  raw_gov_award['date'] = raw_gov_award['date'].astype(int)
  df2 = raw_gov_award[raw_gov_award['date'] >= START_DATE]
  gov_award = pd.concat([gov_award,df2],ignore_index=True)

