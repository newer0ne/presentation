import streamlit as st
import pandas as pd
import chardet

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

pdk = pd.read_excel("pdk.xlsx")
materials = pd.read_excel("Materials.xlsx")
matlist = materials.iloc[:, 1].tolist()

option = st.selectbox(
    'Какой обрабатывался материал?',
    (matlist))

st.write('You selected:', option)

st.dataframe(pdk)
