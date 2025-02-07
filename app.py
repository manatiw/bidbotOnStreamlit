import streamlit as sl
import os
from data_processing.data_cleaner import delete_duplicates
from data_processing.data_exporter import save_dataframes_as_csv

from datetime import datetime
from scrapers.g0vScraper import G0vScraper
from scrapers.pccScraper import PccScraper
from data_processing.pcc_g0v_merger import PccG0vMerger
from config.configLoader import CONFIG_PATH




sl.markdown("<h1 style='text-align: center;'>Moldev相關標案下載</h1>", unsafe_allow_html=True)
sl.markdown("---")


#Display keywords and might open for keyword editing
tk = sl.text_area("title kw")
ck = sl.text_area("company kw")


with sl.form("設定"):
    start_date = sl.date_input("開始日期", value=None)
    sl.checkbox("AI選擇相關標案(not yet deployed)", value=True)
    s_state = sl.form_submit_button("完成設定")
    if s_state:
        if start_date is None or start_date > datetime.now().date():
            sl.warning("請輸入有效開始日期！")
        else:
            formatted_date = int(start_date.strftime("%Y%m%d"))

            g0vScraper = G0vScraper(formatted_date, CONFIG_PATH)
            g0vTenderDf, g0vAwardDf = g0vScraper.run_scraper()

            pccScraper = PccScraper(formatted_date, CONFIG_PATH)
            pccTenderDf, pccAwardDf = pccScraper.run_scraper()

            scrapeDataMerger = PccG0vMerger(pccTenderDf, pccAwardDf, g0vTenderDf, g0vAwardDf)
            tenders_df, awards_df = scrapeDataMerger.run_merger()

            #preview button
            sl.write("tenders_df:")
            sl.write(tenders_df)
            sl.write("awards_df:")
            sl.write(awards_df)

            delete_duplicates(tenders_df, awards_df)
            sl.write("cleaned_df:")
            sl.write(tenders_df)
            sl.write(awards_df)


            #progrss bar move to scraper.py
            bar=sl.progress(0)

            save_csv = sl.button("下載csv")
            if save_csv:
                save_dataframes_as_csv(tenders_df, awards_df)