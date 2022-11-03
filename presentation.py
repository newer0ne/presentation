from asyncore import write
import streamlit as st
from gsheetsdb import connect
import pandas as pd
import io
import requests
from io import StringIO

conn = connect()
@st.cache(ttl=1200)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

class Dataset:
    def __init__(self) -> None:
        self.name = []  
        self.df = []
        self.dfd = []
        self.listcols = []
        self.link = []
        self.up = None
    
    def Open(self, index):
        self.df = pd.read_csv(index)
        self.name = index
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        self.df.drop_duplicates()

    def linkup(self, index):
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

    def Lcols(self):
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])

    def DFinfo (self):
        st.write('Обзор  датафрейма', self.name, ':')
        st.dataframe(self.df)
        st.write('Сведения о датафрейме ', self.name, ':')
        i = self.df
        x = io.StringIO()
        i.info(buf = x)
        i = x.getvalue()
        st.text(i)

    def Unique (self):
        st.markdown("<h4 style='text-align: center;'>Уникальные значения</h4>", unsafe_allow_html=True)
        st.write('Для колонок ниже:')
        x = len(self.listcols)
        unicols = []
        for i in range(x):
            unicols.append(self.name + '_' + self.listcols[i])
        unicols = st.columns(x)
        for ii in range(x):
            unicols[ii].text(self.listcols[ii])
            unicols[ii].text(len(self.df.iloc[:, ii].unique()))
            unicols[ii].write(self.df.iloc[:, ii].unique())

    def renamecol(self, oldname, newname):
        self.df[newname] = self.df[oldname]
        del self.df[oldname]
        self.listcols.remove(oldname)
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        st.text(self.listcols)
        st.dataframe(self.df)

st.markdown("<h2 style='text-align: center;'>Datalyzer</h2>", unsafe_allow_html=True)

headcol1, headcol2 = st.columns(2)

with headcol1:
    header_tasklink = """[<h5 style='text-align: center;'>Test task</h5>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
    st.markdown(header_tasklink, unsafe_allow_html=True)

with headcol2:
    header_repolink = """[<h5 style='text-align: center;'>Github repo this project</h5>](https://github.com/newer0ne/presentation/blob/main/presentation.py)"""
    st.markdown(header_repolink, unsafe_allow_html=True)

name_list = ["ads.csv", "leads.csv", "purchases.csv"]
opt_desc = ["Открыть предустановленный набор данных", "Открыть набор данных по ссылке", "Загрузить любой другой набор данных"]

data1 = Dataset()
data1.link = st.secrets["ads"]
data2 = Dataset()
data2.link = st.secrets["leads"]
data3 = Dataset()
data3.link = st.secrets["purchases"]
data23 = Dataset()
data123 = Dataset()

with st.expander('Выбор способа загрузки данных'):
    
    load_option = st.radio(
        "Выбор способа загрузки данных:",
        (opt_desc))

st.markdown("<h4 style='text-align: center;'>Загруженные данные</h4>", unsafe_allow_html=True)

with st.expander('Загруженные данные'):
    if load_option == opt_desc[0]:    
        tab_open1, tab_open2, tab_open3 = st.tabs(name_list)

        with tab_open1:

            data1.Open(name_list[0])

            st.write("""Представленный набор данных представляет 
            статистку по контекстной рекаламе ('d_utm_medium' = 'cpc') 
            в яндекс.директ ('d_utm_source' = 'yandex').""")
            data1.DFinfo()
            data1.Unique()

            st.write("""Колонки 'created_at', 'd_utm_source' и 'd_utm_medium' потребуются для
            операции слияния c таблицей leads.csv как ключевые столбцы.""")
            
            st.write("""Преобразуем типы данных в 'm_clicks' и 'm_cost' в целочисленные.""")

            data1.df = data1.df.drop(columns = ['d_ad_account_id', 'd_utm_term'])
            data1.df['m_cost'] = data1.df['m_cost'].astype(int)
            data1.df['m_clicks'] = data1.df['m_clicks'].astype(int)

            st.markdown("<h4 style='text-align: center;'>Результат преобразований</h4>", unsafe_allow_html=True)
            data1.DFinfo()

        with tab_open2:

            data2.Open(name_list[1])

            st.write("""Представленный набор данных представляет
            статистку по заявкам на сайте. По сути это основная таблица для
            с которой будут осуществляться операции сляиния.""")
            data2.DFinfo()
            data2.Unique()

            st.write("""Колонки 'lead_created_at', 'd_lead_utm_source' и 
            'd_lead_utm_medium' потребуются для операции слияния с таблицей 
            ads.csv а также колонка 'client_id' для операции слияния с таблицей
            purchases.csv как ключевые колонки.""")

            #st.write("""Отсортируем значения в колонке 'd_lead_utm_source' по
            #источнику 'yandex' и 'd_lead_utm_medium' по контексту 'cpc'""")
            #data2.df = data2.df[(data2.df['d_lead_utm_source'] == 'yandex') & (data2.df['d_lead_utm_medium'] == 'cpc')]

            st.write("""Приведем колонку 'client_id' к формату данных str
            и уберем строки с пустымии ячейками в колонках 'client_id' и 
            'd_lead_utm_content', после чего удалим 'd_lead_utm_content',
            т.к. на итоговую статику колонка не повлияет.""")
            data2.df['client_id'] = data2.df['client_id'].astype(str)
            #data2.df = data2.df[(data2.df['client_id'] != 'nan')]
            #data2.df = data2.df[(data2.df['d_lead_utm_content'].notnull())]
            #data2.df = data2.df.drop(columns = ['d_lead_utm_term'])

            st.markdown("<h4 style='text-align: center;'>Результат преобразований</h4>", unsafe_allow_html=True)
            data2.DFinfo()

        with tab_open3:

            data3.Open(name_list[2])

            st.write("""Представленный набор данных представляет
            статистку по оплатам.""")
            data3.DFinfo()
            data3.Unique()

            st.write("""Приведем колонку 'client_id' к формату данных str
            и уберем строки с пустымии ячейками в колонке 'client_id'.""")
            data3.df['client_id'] = data3.df['client_id'].astype(str)
            #data3.df = data3.df[(data3.df['client_id'] != 'nan')]

            st.write("""Приведем колонку 'm_purchase_amount' к формату данных int
            и отобразм в ней строки с со значениями больше нуля.""")
            data3.df['m_purchase_amount'] = data3.df['m_purchase_amount'].astype(int)
            #data3.df = data3.df[(data3.df['m_purchase_amount'] > 0)]
            data3.DFinfo()

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

    if (data1.df is None) or (data2.df is None) or (data3.df is None):
        st.error('This is an error', icon="🚨")

st.markdown("<h4 style='text-align: center;'>Слияние таблиц leads и purchase</h4>", unsafe_allow_html=True)

with st.expander('Слияние таблиц leads + purchase'):
    data23.df = pd.merge(data2.df, data3.df, how = 'left', on = 'client_id')
    data23.Lcols()
    data23.name = name_list[1] + ' & ' + name_list[2]
    data23.DFinfo()

    st.write("""Проведем сортировку данных в колонке 'd_lead_utm_source'
    на наличие источника трафика с 'yandex'.""") #, а также колонку с размером оплаты'm_purchase_amount' больше нуля
    st.write("""Приведем колонки 'd_lead_utm_content', 
    'd_lead_utm_campaign' к фомату данных int.""")# 'm_purchase_amount', 
    data23.df = data23.df[(data23.df['d_lead_utm_source'] == 'yandex')] #& (data23.df['m_purchase_amount'] > 0)
    #data23.df['m_purchase_amount'] = data23.df['m_purchase_amount'].astype(int)
    data23.df['d_lead_utm_content'] = data23.df['d_lead_utm_content'].astype(int)
    data23.df['d_lead_utm_campaign'] = data23.df['d_lead_utm_campaign'].astype(int)

    data23.DFinfo()
    data23.Unique()
    st.write("Количество уникальных заявок", len(data23.df['lead_id'].unique()), 
    "больше, чем количество уникальных клиентов ", len(data23.df['client_id'].unique()), ",",
    "поэтому требуется определить для каких клиентов было заведено несколько заявок.")
    data23.df['dupl'] = data23.df.duplicated(subset=['client_id'])
    data23.dfd = data23.df[data23.df['dupl'] == True]
    st.write("Дубликатов в колонке 'client_id' = ", len(data23.dfd['dupl'] == True), ".")
    st.dataframe(data23.dfd)

st.markdown("<h4 style='text-align: center;'>Слияние таблиц ads + leads_purchase</h4>", unsafe_allow_html=True)

with st.expander('Слияние таблиц ads + leads_purchase'):
    data1.DFinfo()
    data1.df.astype({'m_clicks': 'int'})
    
    #data123.df = pd.merge(data1.df, data23.df, how = 'left', on = ['created_at', 'utm_medium','utm_source', 'utm_campaign', 'utm_content'])
    #data123.DFinfo()

    #st.text("Удаляем стобец 'utm_content', 'purchase_id'.")
    #data123.df = data123.df.drop(columns = ['utm_content', 'purchase_id'])
    #data123.DFinfo()

#    st.text('Определим строки с разницей по оплатам в 15 дней:')

#data123.df['created_at'] = data123.df['created_at'].astype(str)
#data123.df['DATE'] = pd.to_datetime(data123.df['created_at'], infer_datetime_format=True)  
#data123.df['DATE'] = pd.to_datetime(data123.df['DATE'], format = "%y-%m-%d")
#data123.df['DATE_P'] = pd.to_datetime(data123.df['purchase_created_at'], infer_datetime_format=True)  
#data123.df['DATE_P'] = pd.to_datetime(data123.df['DATE_P'], format = "%y-%m-%d")
#data123.df['Difference'] = (data123.df['DATE_P'] - data123.df['DATE']).dt.days
#data123.df = data123.df.drop(columns = ['DATE', 'DATE_P'])
#data123.df = data123.df[(data123.df['Difference'] >= 0)]
#data123.DFinfo()

#st.text('Посмотрим на параметры таблицы после преобразований даты')
#m123['Дата_оплаты'] = datetime.strptime(m123['purchase_created_at'], '%m-%d-%Y').date()
#m123['Difference'] = (m123['Дата'] - m123['Дата_оплаты']).dt.days
#st.dataframe(m123)


#buffer = io.StringIO()
#joined123.info(buf = buffer)
#joined_df_info = buffer.getvalue()
#st.text(joined_df_info)

#df_to_download = joined123.to_csv()
#st.download_button(label='📥 Download .CSV', data = df_to_download, file_name = "Joined dataframe" + ".csv")



#st.write("Dataframe Renamer")
#ren1, ren2, ren3 = st.columns(3)

#with ren1:
#    data4.name = st.radio(
#        "Dataframe selection to rename 👉",
#        (data1.name, data2.name, data3.name))
#    st.write("Choosed dataframe: " + data4.name)

#with ren2:
#    if data4.name == data1.name:
#        ren_col = st.radio(
#            "Columns selection 👉",
#            (data1.listcols))
#        st.write("Choosed column: " + ren_col)
#    elif data4.name == data2.name:
#        ren_col = st.radio(
#            "Columns selection 👉",
#            (data2.listcols))
#        st.write("Choosed column: " + ren_col)
#    elif data4.name == data3.name:
#        ren_col = st.radio(
#            "Columns selection 👉",
#            (data3.listcols))
#        st.write("Choosed column: " + ren_col)

#with ren3:
#    newcolname = st.text_input('New column name', ren_col)
#    st.write("New name for the selected column: " + newcolname)

#if st.button('Lets change it'):
#    if data4.name == name_list[0]:
#        data1.renamecol(ren_col, newcolname)
#    elif data4.name == name_list[1]:
#        data2.renamecol(ren_col, newcolname)
#    elif data4.name == name_list[2]:
#        data3.renamecol(ren_col, newcolname)


#with st.expander("Dataset Joiner"):
#    col4, col5, col6, col7 = st.columns(4)
#
#    with col4:
#        join1 = st.radio(
#            "Выбор первого датафрейма для Join 👉",
#            (data1.name, data2.name, data3.name))

#        if join1 == data1.name:
#            join1_df = data1.df
#        if join1 == data2.name:
#            join1_df = data2.df
#        if join1 == data3.name:
#            join1_df = data3.df

#    with col5:
#        join2 = st.radio(
#            "Выбор второго датафрейма для Join 👉",
#            (data1.name, data2.name, data3.name))

#        if join2 == data1.name:
#            join2_df = data1.df
#        if join2 == data2.name:
#            join2_df = data2.df
#        if join2 == data3.name:
#            join2_df = data3.df

#    with col6:
#        join_type = st.radio(
#            "Выбор типа Join 👉",
#            ("left", "right", "inner","outer"))
#        join_mark = ("Попробуем " + join_type + "join:")

#    with col7:
#        if join_df_2 == "df_ads":
#            join_col_list = list_ads
#        if join_df_2 == "df_leads":
#            join_col_list = list_leads
#        if join_df_2 == "df_purchases":
#            join_col_list = list_purchases
    
#        join_col = st.radio(
#            "Выбор столбца для Join 👉",
#            (join_col_list))

#    st.text("Join columns must have the same name")
#    if st.button('Lets JOIN that!'):
#        st.markdown(join_mark, unsafe_allow_html = True)
#        joined_df = pd.merge(join_df_1_, join_df_2_, how = join_type, on = join_col)
#        st.dataframe(joined_df)

#        buffer = io.StringIO()
#        joined_df.info(buf = buffer)
#        joined_df_info = buffer.getvalue()
#        st.text(joined_df_info)

#        df_to_download = joined_df.to_csv()
#        st.download_button(label='📥 Скачать обработанную ведомость в формате .CSV', data = df_to_download, file_name = "Joined dataframe" + ".csv")

#with st.expander("Dataset Filter"):
#    if st.button('if Joined_df sucsessful'):
#        filter = joined_df


#    uploaded_filter = st.file_uploader("Area to filter df")
#    if uploaded_filter is not None:
#        st.write("Filename: ", uploaded_filter.name)
#        df_filter = pd.read_csv(uploaded_filter)
#        st.markdown("""<h5 style='text-align: center;'>Датасет для фильтрации:</h5>""", unsafe_allow_html = True)
#        st.dataframe(df_filter)

#        cols_filter = df_filter.columns
#        list_filter = []
#        for i in range(len(cols_filter)):
#            list_filter.append(cols_filter[i])

#        st.markdown("""<h5 style='text-align: center;'>Фильтр под задание:</h5>""", unsafe_allow_html = True)
#        #df_filter[(df_filter.m_purchase_amount > 0) & (df_filter.hp > 80)]
#        df_filter2 = df_filter[(df_filter.m_purchase_amount > 0)]

#        df_filter2['datelag'] = 0
#        st.text("added datelag")
#        df_filter2["purchase_created_at"] = pd.to_datetime(df_filter2["purchase_created_at"])
#        df_filter2["lead_created_at"] = pd.to_datetime(df_filter2["lead_created_at"])
#        df_filter2['datelag'] = (df_filter2['purchase_created_at'] - df_filter2['lead_created_at'])
#        df_filter2["datelag"] = df_filter2["datelag"].dt.days
#        st.dataframe(df_filter2)