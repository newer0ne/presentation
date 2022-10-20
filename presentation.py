
import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import openpyxl
import io
from io import BytesIO
import os
import csv
from pyxlsb import open_workbook as open_xlsb
import webbrowser
from PIL import Image

link_test_task = '[Тестовое задание](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)'
st.markdown(link_test_task, unsafe_allow_html=True)

conn = connect()

@ st.cache(ttl=600)

link_ads = st.secrets["ads"]

link_ads

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

rows_ads = run_query(f'SELECT * FROM "{link_ads}"')
ads = pd.DataFrame(rows_ads, dtype=str)
st.dataframe(data = ads)
