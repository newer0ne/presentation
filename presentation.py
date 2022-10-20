
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


#rows_ads = run_query(f'SELECT * FROM "{link_ads}"')
#ads = pd.DataFrame(rows_ads, dtype=str)
#st.dataframe(data=ads)

url=st.secrets["ads"]
file_id=url.split('/')[-2]
dwn_url='https://drive.google.com/uc?id=' + file_id
df = pd.read_csv(dwn_url)
print(df.head())