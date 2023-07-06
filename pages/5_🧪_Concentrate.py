import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

eche = pd.read_excel("eche.xlsx")
#pdk = pd.read_excel("pdk.xlsx")
materials = pd.read_excel("Materials.xlsx")
matlist = materials.iloc[:, 1].tolist()

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
    
Q = amphours / F

calc_mat = materials.loc[materials['Mарка'] == mat_option].copy()
st.write('Химический состав по элементам:')
#calc_mat_stat = calc_mat.dropna(axis='columns')
st.dataframe(calc_mat.dropna(axis='columns'))


calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x * Q) # Получаем моли

for column in calc_mat.columns[2:]:
    element_symbol = column
    calc_mat[column] = calc_mat[column] * molar_mass[element_symbol]
    
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x * 1000) # Получаем милиграммы
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:].apply(lambda x: x / volume) # Получаем милиграммы на литр
calc_mat = calc_mat.round(3)

st.write('Растворено веществ мг/л:')

pdk = {
    'Fe': 2.0,
    'Cr': 0.05,
    'Ni': 0.02,
    'Mn': 0.2,
    'Cu': 0.2,
    'C': 0.09,
    'S': 3.0,
    'P': 1.0,
    'Si': 0.15,
    'Ti': 0.5,
    'Mo': 0.05
}

compare_df = pd.DataFrame(columns=['Элемент', 'Масса, мг/л', 'ПДК, мг/л', 'Превышение'])

element_symbol = []
element_mass = []
element_pdk = []
exceed_limit = []

for column in calc_mat.columns[2:]:
    element_symbol.append(column)
    element_mass.append(calc_mat[column].values[0])
    element_pdk.append(pdk[column])
    exceed_limit.append(bool(element_mass[-1] > element_pdk[-1]))
    
compare_df = pd.DataFrame(list(zip(element_symbol, element_mass, element_pdk, exceed_limit)), columns=['Элемент', 'Масса, мг/л', 'ПДК, мг/л', 'Превышение'])
compare_df = compare_df.sort_values(by=['Превышение'], ascending=False)

st.dataframe(compare_df, use_container_width=True)

chart_data = compare_df[['Элемент','Масса, мг/л', 'ПДК, мг/л']]
#st.bar_chart(chart_data, x='Элемент')

x = np.arange(len(compare_df['Элемент']))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots()

for attribute in compare_df[['Масса, мг/л', 'ПДК, мг/л']]:
    offset = width * multiplier
    rects = ax.bar(x + offset, compare_df[attribute], width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Масса, мг/л')
ax.set_title('Сравнение элементов по массе и ПДК')
ax.set_xticks(x, compare_df['Элемент'])
ax.legend()

st.pyplot(fig)