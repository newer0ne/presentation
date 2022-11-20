import streamlit as st
import pandas as pd

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
    leads = pd.read_csv(uploaded_purchases)

if uploaded_ads is not None and uploaded_leads is not None and uploaded_purchases is not None:
    
    ads_tab, leads_tab, purchases_tab = st.tabs(['ads', 'leads', 'purchases'])

    with ads_tab:
        ads['d_utm_term'] = ads['d_utm_term'].fillna('-')
        ads['created_at'] = pd.to_datetime(ads['created_at'])
        st.dataframe(ads)
    
    with leads_tab:
        ads['d_utm_term'] = ads['d_utm_term'].fillna('-')
        ads['created_at'] = pd.to_datetime(ads['created_at'])
        st.dataframe(ads)
    
    with purchases_tab:
        ads['d_utm_term'] = ads['d_utm_term'].fillna('-')
        ads['created_at'] = pd.to_datetime(ads['created_at'])
        st.dataframe(ads)

