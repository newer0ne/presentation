import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

molar_mass = data['molar_mass']
pdk = data['pdk']
F = data['F']

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# 🧪 ПДК отработавших растворов")
st.write(
    """Расчет соответствия отработавших растворов
    Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК""")

materials = pd.read_excel("materials.xlsx")
matlist = materials.iloc[:, 1].tolist()

col1, col2, col3 = st.columns(3)
with col1:
    mat_option = st.selectbox(
        'Какой обрабатывался материал?',
        (matlist))
    st.write('Обрабатывался:', mat_option)
with col2:
    volume = st.number_input('Объём ванны в литрах:', step=1)
    st.write('Объём ванны:', volume, ' литров')
with col3:
    amphours = st.number_input('Ампер*часы обработки:', step=1)
    st.write(amphours, ' ампер*часов')

Q = amphours / F

calc_mat = pd.DataFrame(materials.loc[materials['Mарка'] == mat_option])
st.write('Химический состав по элементам:')
calc_mat = calc_mat.dropna(axis='columns')
st.dataframe(calc_mat)

# Получаем моли
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:] * Q

for column in calc_mat.columns[2:]:
    element_symbol = column
    calc_mat[column] = calc_mat[column] * molar_mass[element_symbol]

# Получаем милиграммы
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:] * 1000
# Получаем милиграммы на литр
calc_mat.iloc[:, 2:] = calc_mat.iloc[:, 2:] / volume
calc_mat = calc_mat.round(3)

st.write('Растворено веществ мг/л:')

compare_df = pd.DataFrame(columns=['Элемент',
                                   'Масса, мг/л',
                                   'ПДК, мг/л',
                                   'Превышение'])

element_symbol = []
element_mass = []
element_pdk = []
exceed_limit = []

for column in calc_mat.columns[2:]:
    element_symbol.append(column)
    element_mass.append(calc_mat[column].values[0])
    element_pdk.append(pdk[column])
    exceed_limit.append(bool(element_mass[-1] > element_pdk[-1]))

compare_df = pd.DataFrame(list(zip(element_symbol,
                                   element_mass,
                                   element_pdk,
                                   exceed_limit)),
                          columns=['Элемент',
                                   'Масса, мг/л',
                                   'ПДК, мг/л',
                                   'Превышение'])

compare_df['Превышение раз'] = compare_df['Масса, мг/л'] / \
    compare_df['ПДК, мг/л']
compare_df = compare_df.sort_values(by=['Превышение раз'], ascending=False)
st.dataframe(compare_df, use_container_width=True)


st.write('''Ниже приведено сравнение растворенных элементов
         по массе и ПДК в отношении от 0,1:''')

chart_data = compare_df.drop(columns=['Превышение'])
chart_data = chart_data.loc[chart_data['Превышение раз'] > 0.1]

x = np.arange(len(chart_data['Элемент']))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots()

for attribute in chart_data[['Масса, мг/л', 'ПДК, мг/л']]:
    offset = width * multiplier
    rects = ax.bar(x + offset, chart_data[attribute], width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Масса, мг/л')
ax.set_title('Сравнение элементов по массе и ПДК')
ax.set_xticks(x, chart_data['Элемент'])
ax.legend()


st.pyplot(fig)
