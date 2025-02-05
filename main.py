import streamlit as sl
import os
from datetime import datetime
from scrapers.g0vScraper import G0vScraper
from config.configLoader import CONFIG_PATH



sl.markdown("<h1 style='text-align: center;'>Moldev相關標案下載</h1>", unsafe_allow_html=True)
sl.markdown("---")



tk = sl.text_area("title kw")

ck = sl.text_area("company kw")


with sl.form("設定"):
    start_date = sl.date_input("開始日期", value=None)
    sl.checkbox("AI選擇相關標案", value=True)
    s_state = sl.form_submit_button("完成設定")
    if s_state:
        if start_date is None or start_date > datetime.now().date():
            sl.warning("請輸入有效開始日期！")
        else:
            formatted_date = int(start_date.strftime("%Y%m%d"))
            g0vScraper = G0vScraper(formatted_date, CONFIG_PATH)
            df1, df2 = g0vScraper.run_scraper()
            sl.write("DataFrame 1:")
            sl.write(df1)
            sl.write("DataFrame 2:")
            sl.write(df2)



bar=sl.progress(0)

sl.button("下載csv")