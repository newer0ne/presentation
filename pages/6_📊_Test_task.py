import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Test task solution", page_icon="📊", layout="wide", initial_sidebar_state="expanded"
)







st.write(
    """
# 📊 ADS analyzer
Оценка эффективности рекламной компании.
"""
)

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

        ads['d_utm_term'] = ads['d_utm_term'].fillna('-')
        ads['created_at'] = pd.to_datetime(ads['created_at'], format='%Y%m%d', errors='ignore')
        
        st.dataframe(ads)
    
    with leads_tab:
        
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
        
        leads['created_at'] = pd.to_datetime(leads['created_at'], format='%Y%m%d', errors='ignore')

        st.dataframe(leads)
    
    with purchases_tab:

        purchases['purchase_created_at'] = pd.to_datetime(purchases['purchase_created_at'], format='%Y%m%d', errors='ignore')
        purchases.dropna(axis=0, subset=['m_purchase_amount'], inplace=True)
        
        st.dataframe(purchases)

    compose = leads[['client_id', 'created_at', 'lead_id']].merge(purchases, 'left', 'client_id')
    st.dataframe(compose)

    delta = timedelta(days=15)
    delta

    example_delta = compose[['purchase_created_at', 'created_at']]
    example_delta.dropna(axis=0, subset=['purchase_created_at'], inplace=True)
    #example_delta['del'] = example_delta['purchase_created_at'] - example_delta['created_at']
    st.write(example_delta.info())

    #compose = compose.query('purchase_created_at - created_at <= @delta and created_at <= purchase_created_at')
    compose = compose((compose['purchase_created_at'] - compose['created_at'] <= delta) and (compose['created_at'] <= compose['purchase_created_at']))

    compose = compose.sort_values('created_at', ascending=False)\
        .drop_duplicates('purchase_id', keep='first')

    agg_func = {'m_purchase_count': ('purchase_id', 'count'),
        'm_purchase_amount': ('m_purchase_amount', 'sum')}

    compose = compose.groupby('lead_id').agg(**agg_func).reset_index()

    leads_full = leads.merge(compose, 'left', 'lead_id')
