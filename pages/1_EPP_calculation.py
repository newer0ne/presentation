import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="EPP calculation", page_icon="⚗️")

st.markdown("# ⚗️ Калькулятор режимов ЭПП")
st.write(
    """Калькулятор предназначен для быстрой оценки конечной шероховатости при
    электролитно-плазменном полировании стали и цветных сплавов 
    (меди, латуни, алюминия, цинка и их сплавов) не легированных кремнием."""
    )
st.write('Рекомендованный раствора электролита - 5% KNO3, 3% C6H8O7.')

data = pd.read_excel('experement.xlsx')
x = data[['Ra_нач', 't', 'U', 'T']]
y = data['Ra_кон']

# Создайте объект полиномиальных признаков
degree = 2  # Степень полинома
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(x)

model = LinearRegression()
model.fit(X_poly, y)

#coefficients = model.coef_
#intercept = model.intercept_

#print("Коэффициенты:", coefficients)
#print("Перехват:", intercept)

Ra_start = st.slider('Начальная средняя шероховатость Ra, мкм', min_value = 0.8, max_value = 3.2, step=0.1)
time = st.slider('Время обработки t, с', min_value = 60, max_value = 300, step=5)
u = st.slider('Напряжение U, В', min_value = 250, max_value = 450, step=5)
temp = st.slider('Температура Т, °С', min_value = 70, max_value = 90, step=1)

X_new = np.array([[Ra_start, time, u, temp]])
X_new = poly.fit_transform(X_new)
predictions = model.predict(X_new)
Ra_fin = round(predictions[0], 3)
st.write(f"Прогнозируемая шероховатость Ra {Ra_fin} мкм")

# Диапазоны для time и u
time_range = np.arange(60, 301, 30)
u_range = np.arange(250, 451, 25)

# Создание датафрейма
df_new = pd.DataFrame({
    'Ra_start': [Ra_start] * (len(time_range) * len(u_range)),
    'temp': [temp] * (len(time_range) * len(u_range)),
    'time': np.repeat(time_range, len(u_range)),
    'u': np.tile(u_range, len(time_range))
})

# Расчет предсказаний для Ra_кон
X_new = poly.transform(df_new[['Ra_start', 'time', 'u', 'temp']])
predictions = model.predict(X_new)

# Добавление колонки с предсказаниями
df_new['Ra_кон'] = predictions

# Определение минимального и максимального значения в df_new['Ra_кон']
min_value = df_new['Ra_кон'].round(1).min()
max_value = df_new['Ra_кон'].round(1).max()

# Создание контурной диаграммы
fig, ax = plt.subplots()
contour = ax.tricontour(df_new['time'], df_new['u'], df_new['Ra_кон'], levels=np.arange(min_value, max_value, 0.1))

# Нанесение числовых значений на линии контурной диаграммы
plt.clabel(contour, inline=True, fontsize=8, colors='black')

# Добавление красной точки
plt.scatter(time, u, color='red')

# Подпись для красной точки
ax.annotate(f'{Ra_fin} мкм', 
             xy=(time, u), 
             xytext=(time + 0, u + 5), 
             color='red')

# Отображение пользовательской сетки с определенным шагом
x_ticks = np.arange(60, 301, 30)  # Шаг 30 для оси x
y_ticks = np.arange(250, 451, 25)  # Шаг 25 для оси y
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)

# Настройка осей и заголовка
ax.set_xlabel('Время обработки t, c')
ax.set_ylabel('Напряжение U, В')
ax.set_title(f'Ra кон от Ra нач {Ra_start} мкм ({temp} °С)')
ax.grid(True)

# Отображение диаграммы
st.pyplot()