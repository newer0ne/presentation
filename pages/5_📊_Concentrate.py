import streamlit as st
import pandas as pd
import chardet

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

eche = pd.read_excel("eche.xlsx")
pdk = pd.read_excel("pdk.xlsx")
materials = pd.read_excel("Materials.xlsx")
matlist = materials.iloc[:, 1].tolist()

col1, col2, col3 = st.columns(3)

with col1:
    mat_option = st.selectbox(
        'Какой обрабатывался материал?',
        (matlist))
    st.write('Обрабатывался:', mat_option)

with col2:
    volume = st.number_input('Объём ванны в литрах:')
    st.write('Объём ванны:', volume, ' литров')

with col3:
    amphours = st.number_input('Ампер*часы обработки:')
    st.write(amphours, ' ампер*часов')

calc_mat = materials.loc[materials.loc[1] == mat_option]

st.dataframe(calc_mat)
