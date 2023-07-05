import streamlit as st
import pandas as pd
import chardet

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

pdk = pd.read_excel("pdk.xlsx")
materials = pd.read_excel("pdk.xlsx")

option = st.selectbox(
    'Какой обрабатывался материал?',
    (materials['Материал']))

st.write('You selected:', option)

st.dataframe(pdk)
