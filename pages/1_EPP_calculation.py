import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import joblib

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="EPP calculation", page_icon="⚗️")

# Заголовок страницы
st.write("# ⚗️ Калькулятор режимов ЭПП")
st.write(
    """Калькулятор предназначен для быстрой оценки конечной шероховатости при
    электролитно-плазменном полировании стали и цветных сплавов
    (меди, латуни, алюминия, цинка и их сплавов) не легированных кремнием."""
    )
st.write('Рекомендованный раствора электролита - 5% KNO3, 3% C6H8O7.')

# Объект полиномиальных признаков
poly = PolynomialFeatures(degree=2)

# Загрузить модель
model = joblib.load('poly_EPP.pkl')

# Диапазоны для time и u
time_range = np.arange(60, 301, 5)
u_range = np.arange(250, 451, 5)

# Ползунки выбора режима
Ra_s = st.slider(
    'Начальная средняя шероховатость Ra, мкм',
    min_value=0.8,
    max_value=3.2,
    step=0.1)

time = st.slider(
    'Время обработки t, с',
    min_value=60,
    max_value=300,
    step=5)

u = st.slider(
    'Напряжение U, В',
    min_value=250,
    max_value=450,
    step=5)

temp = st.slider(
    'Температура Т, °С',
    min_value=70,
    max_value=90,
    step=1)

# Кнопка перестроения прогноза
btn_recalculate = st.button('Построить прогноз')
if btn_recalculate:
    # Создание датафрейма
    df = pd.DataFrame({
        'Ra_s': [Ra_s] * (len(time_range) * len(u_range)),
        'temp': [temp] * (len(time_range) * len(u_range)),
        'time': np.repeat(time_range, len(u_range)),
        'u': np.tile(u_range, len(time_range))
    })

    # Расчет предсказаний для Ra_кон
    Х = poly.fit_transform(df[['Ra_s', 'time', 'u', 'temp']])
    predictions = model.predict(Х)

    # Добавление колонки с предсказаниями
    df['Ra_f'] = predictions
    df = df.round({'Ra_f': 3})

    Ra_f = df.loc[
        (df['Ra_s'] == Ra_s) & (df['time'] == time)
        & (df['u'] == u) & (df['temp'] == temp),
        'Ra_f'].values[0]
    st.write(f"Прогнозируемая шероховатость Ra {Ra_f} мкм")

    # Определение минимального и максимального значения в df_new['Ra_кон']
    min_value = df['Ra_f'].round(1).min()
    max_value = df['Ra_f'].round(1).max()

    # Создание контурной диаграммы
    fig, ax = plt.subplots()

    contour = ax.tricontour(
        df['time'], df['u'], df['Ra_f'],
        levels=np.arange(min_value, max_value, 0.1))

    # Нанесение числовых значений на линии контурной диаграммы
    plt.clabel(contour, inline=True, fontsize=8, colors='black')

    # Добавление красной точки
    plt.scatter(time, u, color='red')

    # Подпись для красной точки
    ax.annotate(f'{Ra_f} мкм', xy=(time, u),
                xytext=(time + 0, u + 5), color='red')

    # Отображение пользовательской сетки с определенным шагом
    x_ticks = np.arange(60, 301, 30)  # Шаг 30 для оси x
    y_ticks = np.arange(250, 451, 25)  # Шаг 25 для оси y
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Настройка осей и заголовка
    ax.set_xlabel('Время обработки t, c')
    ax.set_ylabel('Напряжение U, В')
    ax.set_title(f'Ra кон от Ra нач {Ra_s} мкм ({temp} °С)')
    ax.grid(True)

    # Отображение диаграммы
    st.pyplot()
