import streamlit as st
import pandas as pd
from gsheetsdb import connect

link_test_task = '[Тестовое задание](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)'
st.markdown(link_test_task, unsafe_allow_html=True)

conn = connect()

@ st.cache(ttl=600)


link_ads = st.secrets["ads"]
link_ads = "https://drive.google.com/file/d/1U7DQGPOEhGWW3aWQHZayF_9ScqBYnaE1/view?usp=sharing"
link_ads

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

rows_ads = run_query(f'SELECT * FROM "{link_ads}"')
ads = pd.DataFrame(rows_ads, dtype=str)
st.dataframe(data = ads)
