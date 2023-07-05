import streamlit as st
import pandas as pd

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

F = 96485 # Кл/моль - Постоянная Фарадея

molar_mass = {
    'Fe': 55.85,
    'Cr': 51.9961,
    'Ni': 58.6934,
    'Mn': 54.938045,
    'Cu': 63.546,
    'C': 12.0107,
    'S': 32.06,
    'P': 30.973761,
    'Si': 28.0855,
    'Ti': 47.867,
    'Mo': 95.96
}

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
    
Q = amphours / F

calc_mat = materials.loc[materials['Mарка'] == mat_option].copy()
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x * Q) # Получаем моли
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x * x.name).multiply(molar_mass, axis=1) # получаем граммы
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x / 1000) # Получаем милиграммы
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x / volume) # Получаем милиграммы на литр

st.dataframe(calc_mat)
