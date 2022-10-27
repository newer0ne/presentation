
from pickle import APPEND
from queue import Empty
import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import io
from io import BytesIO
import requests
from io import StringIO

conn = connect()
@st.cache(ttl=1200)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

st.markdown("<h2 style='text-align: center;'>Datalyzer</h2>", unsafe_allow_html=True)

header_tasklink = """[<h5 style='text-align: center;'>Test task:</h5>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
st.markdown(header_tasklink, unsafe_allow_html=True)

class Dataset:
    def __init__(self) -> None:
        self.name = []  
        self.df = []
        self.listcols = []
        self.link = []
        self.up = None
    
    def open(self, index):
        self.df = pd.read_csv(index)
        st.dataframe(self.df)
        self.name = index
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        st.text(self.listcols)

    def linkup(self, index):
        #link_url = st.secrets[self.link]
        file_id = self.link.split('/')[-2]
        dwn_url = 'https://drive.google.com/uc?export=download&id=' + file_id
        url2 = requests.get(dwn_url).text
        csv_raw = StringIO(url2)
        self.df = pd.read_csv(csv_raw)
        self.name = index
        st.dataframe(self.df)
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        st.text(self.listcols)

    def upload(self, index):
        self.up = st.file_uploader("CSV file upload area, for example " + index)
        if self.up is not None:
            st.write("File name: ", self.up.name)
            self.df = pd.read_csv(self.up)
            st.dataframe(self.df)
            self.name = self.up.name
            for i in range(len(self.df.columns)):
                self.listcols.append(self.df.columns[i])
            st.text(self.listcols)

    def renamecol(self, oldname, newname, data_df, datalist):
        self.df[newname] = self.df[oldname]
        del self.df[oldname]
        data_df = self.df
        self.listcols.remove(oldname)
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        datalist = self.listcols
        st.text(datalist)
        st.dataframe(data_df)


opt_desc = ["Open fixed data from test task", "Link on data from test task", "Upload data whatewer you want"]
load_option = st.radio(
    "Choosing a dataset loading method",
    (opt_desc))

name_list = ["ads.csv", "leads.csv", "purchases.csv"]
data1 = Dataset()
data1.link = st.secrets["ads"]
data2 = Dataset()
data2.link = st.secrets["leads"]
data3 = Dataset()
data3.link = st.secrets["purchases"]
data4 = Dataset()


if load_option == opt_desc[0]:    
    tab_open1, tab_open2, tab_open3 = st.tabs(name_list)    
    with tab_open1:
        data1.open(name_list[0])
    with tab_open2:
        data2.open(name_list[1])    
    with tab_open3:
        data3.open(name_list[2])

elif load_option == opt_desc[1]:
    tab_load1, tab_load2, tab_load3 = st.tabs(name_list)    
    with tab_load1:
        data1.linkup(name_list[0])    
    with tab_load2:
        data2.linkup(name_list[1])        
    with tab_load3:
        data3.linkup(name_list[2])

elif load_option == opt_desc[2]:
    tab_up1, tab_up2, tab_up3 = st.tabs(name_list)
    with tab_up1:
            data1.upload(name_list[0])
    with tab_up2:
            data2.upload(name_list[1])
    with tab_up3:
            data3.upload(name_list[2])


st.write("Dataframe Renamer")
ren1, ren2, ren3 = st.columns(3)

with ren1:
    data4.name = st.radio(
        "Dataframe selection to rename 👉",
        (data1.name, data2.name, data3.name))
    st.write("Choosed dataframe: " + data4.name)

with ren2:
    if data4.name == data1.name:
        ren_col = st.radio(
            "Columns selection 👉",
            (data1.listcols))
        st.write("Choosed column: " + ren_col)
    elif data4.name == data2.name:
        ren_col = st.radio(
            "Columns selection 👉",
            (data2.listcols))
        st.write("Choosed column: " + ren_col)
    elif data4.name == data3.name:
        ren_col = st.radio(
            "Columns selection 👉",
            (data3.listcols))
        st.write("Choosed column: " + ren_col)

with ren3:
    newcolname = st.text_input('New column name', ren_col)
    st.write("New name for the selected column: " + newcolname)

if st.button('Lets change it'):
    if data4.name == name_list[0]:
        data1.renamecol(ren_col, newcolname, data4.df, data4.listcols)
    elif data4.name == name_list[1]:
        data2.renamecol(ren_col, newcolname, data4.df, data4.listcols)
    elif data4.name == name_list[2]:
        data3.renamecol(ren_col, newcolname, data4.df, data4.listcols)

    st.dataframe(data4.df)
    anal_col4 = st.radio(
        "Columns x selection 👉",
        (data4.listcols), key = "anal4")
    st.write("Choosed x column: " + anal_col4)
    st.line_chart(data4.df.loc[:, anal_col4])
    


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