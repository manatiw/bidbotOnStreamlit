import streamlit as sl
import pandas as pd
import re
import scrapers.utils
from bs4 import BeautifulSoup
from config.configLoader import TITLE_KEYWORDS, COMPANY_KEYWORDS, AWARD_SELECTED_COLUMNS, TENDER_SELECTED_COLUMNS, NOT_AWARD_SELECTED_COLUMNS


class PccScraper:
    def __init__(self, start_date, config_path):
        self.config = scrapers.utils.load_config(config_path)
        self.base_url = self.config['websites']['pcc_gov']['baseUrl']
        self.listing_base_url = self.config['websites']['pcc_gov']['listing_base_url']
        self.start_date = start_date
        self.search_year_minguo = (start_date//10000)-1911
    


    def run_scraper(self):
        sl.write("pcc scraper is now running:")

        gov_tender = pd.DataFrame()
        gov_award = pd.DataFrame()
        keyword_placeholder = sl.empty()


        for keyword in TITLE_KEYWORDS:
            keyword_placeholder.text(f"Processing keyword: {keyword}")

            # Tender search result
            tenderQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%8B%9B%E6%A8%99&sortCol=TENDER_NOTICE_DATE&timeRange=" + str(self.search_year_minguo) + "&pageSize=100"

            while True:
                html = scrapers.utils.request(self.listing_base_url + tenderQueryStrings).text
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
                        href = self.base_url + hyperlink
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
                df1 = raw_gov_tender[raw_gov_tender['date'] >= self.start_date]
                gov_tender = pd.concat([gov_tender,df1],ignore_index=True)

                break



            # Award search result
            awardQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%B1%BA%E6%A8%99&sortCol=AWARD_NOTICE_DATE&timeRange=" + str(self.search_year_minguo) + "&pageSize=100"
            html = scrapers.utils.request(self.listing_base_url + awardQueryStrings).text
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
            award_given = None

            i = 0
            for td in tds:
                if i % 10 == 2:
                    org = td.get_text(strip=True)
                    organizations.append(org)
                elif i % 10 == 3:
                    href = td.find('a')
                    hyperlink = href['href']
                    href = self.base_url + hyperlink
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
            df2 = raw_gov_award[raw_gov_award['date'] >= self.start_date]
            gov_award = pd.concat([gov_award,df2],ignore_index=True)



        # Company keyword
        for keyword in COMPANY_KEYWORDS:
            keyword_placeholder.text(f"Processing keyword: {keyword}")
            awardQueryStrings = "?querySentence=" + keyword + "&tenderStatusType=%E6%B1%BA%E6%A8%99&sortCol=AWARD_NOTICE_DATE&timeRange=" + str(self.search_year_minguo) + "&pageSize=100"

            html = scrapers.utils.request(self.listing_base_url + awardQueryStrings).text
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
            award_given = None
            tds = tbody.find_all("td")
            i = 0
            for td in tds:
                if i % 10 == 2:
                    org = td.get_text(strip=True)
                    organizations.append(org)
                elif i % 10 == 3:
                    href = td.find('a')
                    hyperlink = href['href']
                    href = self.base_url + hyperlink
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
            df2 = raw_gov_award[raw_gov_award['date'] >= self.start_date]
            gov_award = pd.concat([gov_award,df2],ignore_index=True)


        return gov_tender, gov_award