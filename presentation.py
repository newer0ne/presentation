
from pickle import APPEND
import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import io
from io import BytesIO
import requests
from io import StringIO

conn = connect()
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

st.markdown("<h2 style='text-align: center;'>Datalyzer</h2>", unsafe_allow_html=True)

header_tasklink = """[<h5 style='text-align: center;'>Test task:</h5>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
st.markdown(header_tasklink, unsafe_allow_html=True)

load_option = "Open fixed data from test task"
load_option = st.radio(
    "Choosing a dataset loading method",
    ("Open fixed data from test task", "Link on data from test task", "Upload data whatewer you want"))

if load_option == "Open fixed data from test task":

    tab_open1, tab_open2, tab_open3 = st.tabs(["ads.csv", "leads.csv", "purchases.csv"])
    
    with tab_open1:

        df_ads = pd.read_csv("ads.csv")
        st.dataframe(df_ads)

        cols_ads = df_ads.columns
        list_ads = []
        for i in range(len(cols_ads)):
            list_ads.append(cols_ads[i])
    
    with tab_open2:
        df_leads = pd.read_csv("leads.csv")
        st.dataframe(df_leads)

        cols_leads = df_leads.columns
        list_leads = []
        for i in range(len(cols_leads)):
            list_leads.append(cols_leads[i])
    
    with tab_open3:
        df_purchases = pd.read_csv("purchases.csv")
        st.dataframe(df_purchases)

        cols_purchases = df_purchases.columns
        list_purchases = []
        for i in range(len(cols_purchases)):
            list_purchases.append(cols_purchases[i])

elif load_option == "Link on data from test task":
    with st.expander("ads.csv"):
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
    
    with st.expander("leads.csv"):
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
        
    with st.expander("purchases.csv"):
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

elif load_option == "Upload data whatewer you want":
    uploaded_ads = st.file_uploader("Область загрузки для ADS.CSV")
    with st.expander("upload ads.csv"):
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
    with st.expander("upload leads.csv"):
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
    with st.expander("upload leads.csv"):
        if uploaded_purchases is not None:
            st.write("Filename: ", uploaded_purchases.name)
            df_purchases = pd.read_csv(uploaded_purchases, sheet_name = "Sheet1", dtype = {'Note': str})
            st.markdown("""<h5 style='text-align: center;'>Второй датасет LEADS:</h5>""", unsafe_allow_html = True)
            st.dataframe(df_purchases)
            cols_purchases = df_purchases.columns
            list_purchases = []
            for i in range(len(cols_purchases)):
                list_purchases.append(cols_purchases[i])

with st.expander("Dataset Analyzer"):
    col1, col2, col3 = st.columns(3)
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
        X_colunm = st.radio(
            "Выбор столбца по оси X",
            (selected_cols))

    with col3:
        Y_colunm = st.radio(
            "Выбор столбца по оси Y",
            (selected_cols))

    if X_colunm == Y_colunm:
        st.error('Выбраны одинаковые столбцы, выберите другие значения', icon="🚨")

    if X_colunm != Y_colunm:
        col4, col5 = st.columns(2)
        with col4:
            chart_df = filtred_df.loc[:, [X_colunm, Y_colunm]]
            st.line_chart(chart_df)
        with col5:
            st.dataframe(chart_df)

with st.expander("Dataset Joiner"):
    col4, col5, col6, col7 = st.columns(4)
    with col4:
        join_df_1 = st.radio(
            "Выбор первого датафрейма для Join 👉",
            ("df_ads", "df_leads", "df_purchases"))
        if join_df_1 == "df_ads":
            join_df_1_ = df_ads
        if join_df_1 == "df_leads":
            join_df_1_ = df_leads
        if join_df_1 == "df_purchases":
            join_df_1_ = list_purchases

    with col5:
        join_df_2 = st.radio(
            "Выбор второго датафрейма для Join 👉",
            ("df_ads", "df_leads", "df_purchases"))
        if join_df_2 == "df_ads":
            join_df_2_ = df_ads
        if join_df_2 == "df_leads":
            join_df_2_ = df_leads
        if join_df_2 == "df_purchases":
            join_df_2_ = df_purchases

    with col6:
        join_type = st.radio(
            "Выбор типа Join 👉",
            ("left", "right", "inner","outer"))
        join_mark = ("Попробуем " + join_type + "join:")

    with col7:
        if join_df_2 == "df_ads":
            join_col_list = list_ads
        if join_df_2 == "df_leads":
            join_col_list = list_leads
        if join_df_2 == "df_purchases":
            join_col_list = list_purchases
    
        join_col = st.radio(
            "Выбор столбца для Join 👉",
            (join_col_list))

    st.text("Join columns must have the same name")
    if st.button('Lets JOIN that!'):
        st.markdown(join_mark, unsafe_allow_html = True)
        joined_df = pd.merge(join_df_1_, join_df_2_, how = join_type, on = join_col)
        st.dataframe(joined_df)

        buffer = io.StringIO()
        joined_df.info(buf = buffer)
        joined_df_info = buffer.getvalue()
        st.text(joined_df_info)

        df_to_download = joined_df.to_csv()
        st.download_button(label='📥 Скачать обработанную ведомость в формате .CSV', data = df_to_download, file_name = "Joined dataframe" + ".csv")

with st.expander("Dataset Filter"):
    if st.button('if Joined_df sucsessful'):
        filter = joined_df


    uploaded_filter = st.file_uploader("Area to filter df")
    if uploaded_filter is not None:
        st.write("Filename: ", uploaded_filter.name)
        df_filter = pd.read_csv(uploaded_filter)
        st.markdown("""<h5 style='text-align: center;'>Датасет для фильтрации:</h5>""", unsafe_allow_html = True)
        st.dataframe(df_filter)

        cols_filter = df_filter.columns
        list_filter = []
        for i in range(len(cols_filter)):
            list_filter.append(cols_filter[i])

        st.markdown("""<h5 style='text-align: center;'>Фильтр под задание:</h5>""", unsafe_allow_html = True)
        #df_filter[(df_filter.m_purchase_amount > 0) & (df_filter.hp > 80)]
        df_filter2 = df_filter[(df_filter.m_purchase_amount > 0)]

        df_filter2['datelag'] = 0
        st.text("added datelag")
        df_filter2["purchase_created_at"] = pd.to_datetime(df_filter2["purchase_created_at"])
        df_filter2["lead_created_at"] = pd.to_datetime(df_filter2["lead_created_at"])
        df_filter2['datelag'] = (df_filter2['purchase_created_at'] - df_filter2['lead_created_at'])
        df_filter2["datelag"] = df_filter2["datelag"].dt.days
        st.dataframe(df_filter2)