
from pickle import APPEND
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


link_Dynam_video_toclic = """[<h2 style='text-align: center;'>Тестовове задание:</h2>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
st.markdown(link_Dynam_video_toclic, unsafe_allow_html=True)

load_option = "open"
load_option = st.radio(
    "Выбор способа загрузки датасета",
    ("open", "link", "upload"))

if load_option == "open":
    df_ads = pd.read_csv("ads.csv")
    st.markdown("""<h5 style='text-align: center;'>Первый датасет ADS:</h5>""", unsafe_allow_html = True)
    st.dataframe(df_ads)
    cols_ads = df_ads.columns
    list_ads = []
    for i in range(len(cols_ads)):
        list_ads.append(cols_ads[i])
    
    df_leads = pd.read_csv("leads.csv")
    st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)
    st.dataframe(df_leads)
    cols_leads = df_leads.columns
    list_leads = []
    for i in range(len(cols_leads)):
        list_leads.append(cols_leads[i])
    
    df_purchases = pd.read_csv("purchases.csv")
    st.dataframe(df_purchases)
    cols_purchases = df_purchases.columns
    list_purchases = []
    for i in range(len(cols_purchases)):
        list_purchases.append(cols_purchases[i])

elif load_option == "link":
    url_ads = st.secrets["ads"]
    file_id_ads = url_ads.split('/')[-2]
    dwn_url_ads = 'https://drive.google.com/uc?export=download&id=' + file_id_ads
    url2_ads = requests.get(dwn_url_ads).text
    csv_raw_ads = StringIO(url2_ads)
    df_ads = pd.read_csv(csv_raw_ads)
    st.markdown("""<h5 style='text-align: center;'>Первый датасет ADS:</h5>""", unsafe_allow_html = True)
    st.dataframe(df_ads)
    cols_ads = df_ads.columns
    list_ads = []
    for i in range(len(cols_ads)):
        list_ads.append(cols_ads[i])
    
    url_leads = st.secrets["leads"]
    file_id_leads = url_leads.split('/')[-2]
    dwn_url_leads = 'https://drive.google.com/uc?export=download&id=' + file_id_leads
    url2_leads = requests.get(dwn_url_leads).text
    csv_raw_leads = StringIO(url2_leads)
    df_leads = pd.read_csv(csv_raw_leads)
    st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)
    st.dataframe(df_leads)
    cols_leads = df_leads.columns
    list_leads = []
    for i in range(len(cols_leads)):
	    list_leads.append(cols_leads[i])
    
    url_purchases = st.secrets["purchases"]
    file_id_purchases = url_purchases.split('/')[-2]
    dwn_url_purchases = 'https://drive.google.com/uc?export=download&id=' + file_id_purchases
    url2_purchases = requests.get(dwn_url_purchases).text
    csv_raw_purchases = StringIO(url2_purchases)
    df_purchases = pd.read_csv(csv_raw_purchases)
    #df_purchases = df_purchases.reindex(columns=['client_id', 'purchase_id', 'purchase_created_at', 'm_purchase_amount'])
    st.markdown("""<h5 style='text-align: center;'>Третий датасет PURCHASES:</h5>""", unsafe_allow_html = True)
    st.dataframe(df_purchases)
    cols_purchases = df_purchases.columns
    list_purchases = []
    for i in range(len(cols_purchases)):
    	list_purchases.append(cols_purchases[i])

elif load_option == "upload":
    uploaded_ads = st.file_uploader("Область загрузки для ADS.CSV")
    if uploaded_ads is not None:
        st.write("Filename: ", uploaded_ads.name)
        df_ads = pd.read_csv(uploaded_ads, sheet_name = "Sheet1", dtype = {'Note': str})
        st.markdown("""<h5 style='text-align: center;'>Первый датасет ADS:</h5>""", unsafe_allow_html = True)
        st.dataframe(df_ads)
        cols_ads = df_ads.columns
        list_ads = []
        for i in range(len(cols_ads)):
            list_ads.append(cols_ads[i])

    uploaded_leads = st.file_uploader("Область загрузки для LEADS.CSV")
    if uploaded_leads is not None:
        st.write("Filename: ", uploaded_leads.name)
        df_leads = pd.read_csv(uploaded_leads, sheet_name = "Sheet1", dtype = {'Note': str})
        st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)
        st.dataframe(df_leads)
        cols_leads = df_leads.columns
        list_leads = []
        for i in range(len(cols_leads)):
            list_leads.append(cols_leads[i])

    uploaded_purchases = st.file_uploader("Область загрузки для PURCHASES.CSV")
    if uploaded_purchases is not None:
        st.write("Filename: ", uploaded_purchases.name)
        df_purchases = pd.read_csv(uploaded_purchases, sheet_name = "Sheet1", dtype = {'Note': str})
        st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)
        st.dataframe(df_purchases)
        cols_purchases = df_purchases.columns
        list_purchases = []
        for i in range(len(cols_purchases)):
            list_purchases.append(cols_purchases[i])

col1, col2 = st.columns(2)

with col1:
    selected_df = st.radio(
        "Выбор датасета 👉",
        ("ads", "leads", "purchases"))

if selected_df == "ads":
    filtred_df = df_ads
    selected_cols = list_ads
elif selected_df == "leads":
    filtred_df = df_leads
    selected_cols = list_leads
elif selected_df == "purchases":
    filtred_df = df_purchases
    selected_cols = list_purchases


with col2:
    X_colunm = st.selectbox(
        "Выбор столбца по оси X",
        (selected_cols))

    selected_cols_Y = selected_cols
    selected_cols_Y.remove(X_colunm)
    
    Y_colunm = st.selectbox("Выбор столбца по оси Y", (selected_cols_Y))

st.dataframe(filtred_df.loc[:, [X_colunm, Y_colunm]])

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.markdown("<h5 style='text-align: center;'>Попробуем левтджоин для сведения всех продаж:</h5>", unsafe_allow_html = True)
df_leads_purchases = pd.merge(df_leads, df_purchases, how = 'left', on = ['client_id'])
st.dataframe(df_leads_purchases)
