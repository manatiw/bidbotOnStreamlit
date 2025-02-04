import streamlit as sl

sl.title("Moldev相關政府採購標案下載")
sl.markdown("---")

sd=sl.date_input("開始日期")

tk=sl.text_area("title kw")


ck=sl.text_area("company kw")
sl.checkbox("AI選擇相關標案", value=True)

sl.button("完成設定")


bar=sl.progress(0)

sl.button("下載csv")