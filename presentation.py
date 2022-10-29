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

st.markdown("<h2 style='text-align: center;'>Datalyzer</h2>", unsafe_allow_html=True)

headcol1, headcol2 = st.columns(2)

with headcol1:
    header_tasklink = """[<h5 style='text-align: center;'>Test task:</h5>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
    st.markdown(header_tasklink, unsafe_allow_html=True)

with headcol2:
    header_repolink = """[<h5 style='text-align: center;'>Github repo this project:</h5>](https://github.com/newer0ne/presentation/blob/main/presentation.py)"""
    st.markdown(header_repolink, unsafe_allow_html=True)


class Dataset:
    def __init__(self) -> None:
        self.name = []  
        self.df = []
        self.dfi = []
        self.listcols = []
        self.link = []
        self.up = None
    
    def open(self, index):
        self.df = pd.read_csv(index)
        st.dataframe(self.df)
        self.name = index
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        st.write("Названия столбцов в dataframe:")
        st.write(self.listcols)
        st.write("Количество строк в таблице: ", len(self.df.axes[0]))


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

    def renamecol(self, oldname, newname):
        self.df[newname] = self.df[oldname]
        del self.df[oldname]
        self.listcols.remove(oldname)
        for i in range(len(self.df.columns)):
            self.listcols.append(self.df.columns[i])
        st.text(self.listcols)
        st.dataframe(self.df)


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

        data1.df['m_clicks'] = data1.df['m_clicks'].astype(int)
        data1.df = data1.df[data1.df['m_clicks'] > 0]
        data1.df['m_cost'] = data1.df['m_cost'].astype(int)
        del data1.df['account_id']
        del data1.df['utm_term']
        st.dataframe(data1.df)

    with tab_open2:
        data2.open(name_list[1])

        del data2.df['utm_term']
        data2.df = data2.df[(data2.df['utm_source'] == 'yandex') & (data2.df['utm_medium'] == 'cpc')]
        data2.df['client_id'] = data2.df['client_id'].astype(str)
        data2.df = data2.df[(data2.df['client_id'] != 'nan')]
        data2.df = data2.df[(data2.df['utm_content'].notnull())]

# Отправить в def dtinfo например
#
#        buffer2 = io.StringIO()
#        data2.dfi = data2.df
#        data2.dfi.info(buf = buffer2)
#        data2.dfi = buffer2.getvalue()
#        st.text(data2.dfi)
#        st.dataframe(data2.df)

# Пригодится под цикл уникальных значений в столбцах
# for i in range(len(self.df.columns)):
#
#        self.colop1, self.colop2, self.colop3, self.colop4, self.colop5, self.colop6 = st.columns(6)

#        self.colop1.write("Уникальные значения в столбце 1: ")
#        self.colop1.dataframe(self.df.iloc[:, 0].unique())
#        self.colop2.write("Уникальные значения в столбце 2: ")
#        self.colop2.dataframe(self.df.iloc[:, 1].unique())
#        self.colop3.write("Уникальные значения в столбце 3: ")
#        self.colop3.dataframe(self.df.iloc[:, 2].unique())
#        self.colop4.write("Уникальные значения в столбце 4: ")
#        self.colop4.dataframe(self.df.iloc[:, 3].unique())
#        self.colop5.write("Уникальные значения в столбце 5: ")
#        self.colop5.dataframe(self.df.iloc[:, 4].unique())
#        self.colop6.write("Уникальные значения в столбце 6: ")
#        self.colop6.dataframe(self.df.iloc[:, 5].unique())

    with tab_open3:
        data3.open(name_list[2])    

        data3.df['client_id'] = data3.df['client_id'].astype(str)
        data3.df = data3.df[(data3.df['client_id'] != 'nan')]
        data3.df['m_purchase_amount'] = data3.df['m_purchase_amount'].astype(int)
        data3.df = data3.df[(data3.df['m_purchase_amount'] > 0)]

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


m23 = pd.merge(data2.df, data3.df, how = 'left', on = 'client_id')

st.write("Фильтрованная таблица по типам данных astype(int), 'utm_source' == 'yandex' и 'm_purchase_amount'] > 0:")

m23f = m23[(m23['utm_source'] == 'yandex') & (m23['m_purchase_amount'] > 0)]
m23f['m_purchase_amount'] = m23f['m_purchase_amount'].astype(int)
m23f['utm_content'] = m23f['utm_content'].astype(int)
m23f['utm_campaign'] = m23f['utm_campaign'].astype(int)
st.dataframe(m23f)

st.write("Типы данных merget tables после обработки:")

buffer4 = io.StringIO()
m23i = m23f
m23i.info(buf = buffer4)
m23i = buffer4.getvalue()
st.text(m23i)

st.writet("Подготовка типов данных для merge ads + leads_purchase:")

data1.df.astype({'m_clicks': 'int'})
buffer5 = io.StringIO()
data1.dfi = data1.df
data1.dfi.info(buf = buffer5)
data1.dfi = buffer5.getvalue()
st.text(data1.dfi)

m123 = pd.merge(data1.df, m23f, how = 'left', on = ['created_at', 'utm_medium','utm_source', 'utm_campaign', 'utm_content'])
#m123 = m123[(m123.m_purchase_amount > 0)]
#m123['m_purchase_amount'] = m123['m_purchase_amount'].astype(int)

st.text("Типы данных merget tables ads_leads_purchase:")

buffer6 = io.StringIO()
m123i = m123
m123i.info(buf = buffer6)
m123i = buffer6.getvalue()
st.text(m123i)

st.text("Удаляем стобец 'utm_content':")

del m123['utm_content']
st.dataframe(m123)

st.text('Определим строки с разницей по оплатам в 15 дней:')

m123['created_at'] = m123['created_at'].astype(str)
m123['DATE'] = pd.to_datetime(m123['created_at'], infer_datetime_format=True)  
m123['DATE'] = pd.to_datetime(m123['DATE'], format = "%y-%m-%d")
m123['DATE_P'] = pd.to_datetime(m123['purchase_created_at'], infer_datetime_format=True)  
m123['DATE_P'] = pd.to_datetime(m123['DATE_P'], format = "%y-%m-%d")
m123['Difference'] = (m123['DATE_P'] - m123['DATE']).dt.days
m123 = m123[(m123.Difference >= 0) & (m123.Difference <= 15)]

buffer7 = io.StringIO()
m123ii = m123
m123ii.info(buf = buffer7)
m123ii = buffer7.getvalue()

st.text('Посмотрим на параметры таблицы после преобразований даты')
st.dataframe(m123)
st.text(m123ii)

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