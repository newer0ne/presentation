
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


link_Dynam_video_toclic = '[Тестовое задание](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)'
st.markdown(link_Dynam_video_toclic, unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center;'>Первый датасет ADS:</h5>""", unsafe_allow_html=True)

url=st.secrets["ads"]
file_id = url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
url2 = requests.get(dwn_url).text
csv_raw = StringIO(url2)
df = pd.read_csv(csv_raw)
st.dataframe(df)