
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
from PIL import Image
import requests
from io import StringIO

conn = connect()
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0,00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


link_Dynam_video_toclic = '["""<h5 style='text-align: center;'>Тестовое задание:</h5>"""](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)'
st.markdown(link_Dynam_video_toclic, unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center;'>Первый датасет ADS:</h5>""", unsafe_allow_html = True)

url_ads = st.secrets["ads"]
file_id_ads = url_ads.split('/')[-2]
dwn_url_ads = 'https://drive.google.com/uc?export=download&id=' + file_id_ads
url2_ads = requests.get(dwn_url_ads).text
csv_raw_ads = StringIO(url2_ads)
df_ads = pd.read_csv(csv_raw_ads)
st.dataframe(df_ads)

st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)

url_leads = st.secrets["leads"]
file_id_leads = url_leads.split('/')[-2]
dwn_url_leads = 'https://drive.google.com/uc?export=download&id=' + file_id_leads
url2_leads = requests.get(dwn_url_leads).text
csv_raw_leads = StringIO(url2_leads)
df_leads = pd.read_csv(csv_raw_leads)
st.dataframe(df_leads)

st.markdown("""<h5 style='text-align: center;'>Третий датасет PURCHASES:</h5>""", unsafe_allow_html = True)

url_purchases = st.secrets["purchases"]
url_purchases
file_id_purchases = url_purchases.split('/')[-2]
dwn_url_purchases = 'https://drive.google.com/uc?export=download&id=' + file_id_purchases
url2_purchases = requests.get(dwn_url_purchases).text
csv_raw_purchases = StringIO(url2_purchases)
df_purchases = pd.read_csv(csv_raw_purchases)
st.dataframe(df_purchases)