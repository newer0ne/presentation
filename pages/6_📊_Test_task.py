import streamlit as st
from 2_📄_Datalyzer_workspase import open

st.set_page_config(
    page_title="Test task solution", page_icon="📊", initial_sidebar_state="expanded"
)







st.write(
    """
# 📊 ADS analyzer
Загрузите данные, чтобы увидеть эффективность рекламной компании.
"""
)

upcol1, upcol2, upcol3 = st.columns(3)

with upcol1:
    uploaded_ads = st.file_uploader("Загрузка .CSV фалов", type=".csv")

with upcol2:
    uploaded_leads = st.file_uploader("Загрузка .CSV фалов", type=".csv")

with upcol3:
    uploaded_purchases = st.file_uploader("Загрузка .CSV фалов", type=".csv")

use_example = st.checkbox(
    "Использовать файл с примером", False, help="Используйте встроенный файл с примером рекламы для демонстрации работы приложения"
)

if use_example:
    uploaded_ads = "ads.csv"
    uploaded_leads = "leads.csv"
    uploaded_purchases = "purchases.csv"

    