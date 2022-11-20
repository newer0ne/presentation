import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import StringIO

st.set_page_config(
    page_title="Test task in work", page_icon="📊", layout="wide", initial_sidebar_state="expanded"
)

st.write(
    """
# 📊 ADS analyzer
Оценка эффективности рекламной компании.
"""
)

#tasklink = """[Тестовое задание.](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
#st.markdown(tasklink, unsafe_allow_html=True)

upcol1, upcol2, upcol3 = st.columns(3)

with upcol1:
    uploaded_ads = st.file_uploader("Загрузка рекламной компании .CSV", type=".csv")

with upcol2:
    uploaded_leads = st.file_uploader("Загрузка лидов .CSV", type=".csv")

with upcol3:
    uploaded_purchases = st.file_uploader("Загрузка продаж .CSV", type=".csv")

use_example = st.checkbox(
    "Использовать файл с примером", False, help="Используйте встроенный файл с примером рекламы для демонстрации работы приложения"
)

if use_example:
    uploaded_ads = "ads.csv"
    uploaded_leads = "leads.csv"
    uploaded_purchases = "purchases.csv"

if uploaded_ads:
    ads = pd.read_csv(uploaded_ads)
if uploaded_leads:
    leads = pd.read_csv(uploaded_leads)
if uploaded_purchases:
    purchases = pd.read_csv(uploaded_purchases)

if uploaded_ads is not None and uploaded_leads is not None and uploaded_purchases is not None:
    
    ads_tab, leads_tab, purchases_tab = st.tabs(['ads', 'leads', 'purchases'])

    with ads_tab:
        
        st.markdown('#### Исходный датафрейм ads')
        st.dataframe(ads)

        ads['d_utm_term'] = ads['d_utm_term'].fillna('-')
        ads['created_at'] = pd.to_datetime(ads['created_at'], format = '%Y-%m-%d', errors = 'ignore')
        
        st.markdown('#### Реклам: Заменяем пропуски, приводим даты')
        st.dataframe(ads)
    
    with leads_tab:

        st.markdown('#### Исходный датафрейм leads')
        st.dataframe(leads)
        
        leads.fillna({'d_lead_utm_source': '-',
            'd_lead_utm_medium': '-',
            'd_lead_utm_campaign': '-',
            'd_lead_utm_content': '-',
            'd_lead_utm_term': '-'}, inplace=True)
        
        leads.rename(columns = {'d_lead_utm_source': 'd_utm_source',
            'd_lead_utm_medium': 'd_utm_medium',
            'd_lead_utm_campaign': 'd_utm_campaign',
            'd_lead_utm_content': 'd_utm_content',
            'd_lead_utm_term': 'd_utm_term',
            'lead_created_at': 'created_at'}, inplace=True)
        
        leads['created_at'] = pd.to_datetime(leads['created_at'], format = '%Y-%m-%d', errors = 'ignore')

        st.markdown('#### Лиды: Заменяем пропуски, переименовываем, приводим даты')
        st.dataframe(leads)
    
    with purchases_tab:
        
        st.markdown('### Исходный датафрейм purchases')
        st.dataframe(purchases)

        purchases['purchase_created_at'] = pd.to_datetime(purchases['purchase_created_at'], format = '%Y-%m-%d', errors = 'ignore')
        purchases.dropna(axis=0, subset=['m_purchase_amount'], inplace=True)
        
        st.markdown('#### Продажи: убираем пустые продажи, приводим даты')
        st.dataframe(purchases)

    st.markdown(
        """
        #### Объединяем лиды и продажи:

        - Лиду засчитывается продажа не позднее 15 дней
        - purchase_id не может повторяться
        - Часть лидов может потеряться, когда мы делаем drop_duplicates
        """
        )

    compose = leads[['client_id', 'created_at', 'lead_id']].merge(purchases, 'left', 'client_id')
    
    delta = timedelta(days=15)

    compose = compose.query('purchase_created_at - created_at <= @delta and created_at <= purchase_created_at')

    compose = compose.sort_values('created_at', ascending=False)\
        .drop_duplicates('purchase_id', keep='first')

    agg_func = {'m_purchase_count': ('purchase_id', 'count'),
        'm_purchase_amount': ('m_purchase_amount', 'sum')}

    compose = compose.groupby('lead_id').agg(**agg_func).reset_index()

    leads_full = leads.merge(compose, 'left', 'lead_id')
    st.dataframe(leads_full)

    compose.lead_id.nunique(), leads_full.lead_id.nunique()

    st.markdown('#### Агрегируем рекламу и лидов по тем полям, которые используются для джойна')

    columns_to_groupby = ['created_at',
                      'd_utm_source',
                      'd_utm_medium',
                      'd_utm_campaign',
                      'd_utm_content',
                      'd_utm_term'] 
    agg_func = {'m_clicks': ('m_clicks', 'sum'),
           'm_cost': ('m_cost', 'sum')}

    ads = ads.groupby(columns_to_groupby).agg(**agg_func).reset_index()
    ads.d_utm_campaign = ads.d_utm_campaign.astype('str')
    ads.d_utm_content = ads.d_utm_content.astype('str')

    agg_func = {'m_leads_count': ('lead_id', 'nunique'),
            'm_purchase_count': ('m_purchase_count', 'sum'),
           'm_purchase_amount': ('m_purchase_amount', 'sum')}

    leads_full = leads_full.groupby(columns_to_groupby).agg(**agg_func).reset_index()

    st.dataframe(leads_full)

    st.markdown('#### Джойн рекламы и лидов, считаем доп метрики')

    result = ads.merge(leads_full, 'outer', columns_to_groupby)
    result.fillna(0, inplace=True)

    result['cpl'] = np.where(result['m_leads_count'] != 0,
        result['m_cost'] / result['m_leads_count'],
        0)

    result['roas'] = np.where(result['m_cost'] != 0,
        result['m_purchase_amount'] / result['m_cost'],
        0)

    result[result['cpl'] > 0]
