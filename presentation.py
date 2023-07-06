import streamlit as st
import time

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

st.markdown("<h1 style='text-align: center;'>Привет и добро пожаловать в Datalyzer! 👋</h1>", unsafe_allow_html=True)

st.markdown(
    """
    Datalyzer — это проект по подготовке датафреймов для сквозной
    аналитики данных и последующей их визуализации.

    ### Как это работает?
    Для работы алгоритмов нужен хороший интернет,
    и если его нет - придётся немного подождать 🥲

    ### Слева расположен сайдбар с выбором вкладок:
    - «ADS analyzer» - обрабатка датафреймов для сквозной аналитики продажи-лиды-покупки.
    - «АВ Tester» - Анализ результатов A/B теста с графическим отображением
        результата и вычислением основных параметров.
    - «Plotting graf» - рандомизированный график.
    - «DataFrame visualizer» - визуализатор датафреймов.
        Для примера взято валовое сельскохозяйственное производство по годам.
    - «Concentrate» - Калькулятор ПДК отработавших растворов электролита.

    ### Что дальше?
    - «ADS analyzer»: 
        расширение функционала модуля загрузок, 
        внутренний управляемый ренейм колонок.
    - «Plotting graf»:
        добавление модуля загрузок по ссылке / датафреймом,
        выбор типа графика для загруженных данных,
        регрессионный анализ.
    - «DataFrame visualizer»:
        Добавление выбора стандартных баз данных для отображения.

    ## Хотите знать немного больше об авторе?
    - Мои работы:
        - [Классификатор для РОСАТОМА](https://classificator.streamlit.app/)        
    - Здесь мои социальные сети:
        - [telegram.org](https://t.me/newer0ne)
        - [linkedin.com](https://www.linkedin.com/in/zakharovsv/)
        - [vk.com](https://vk.com/id1237712)
        - [github.com](https://github.com/newer0ne)
    - Контакты на рекрутинговых платформах:
        - [headhunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
        - [career.habr.com](https://career.habr.com/sergeyzaharov123)
    - Если возникли какие-то вопросы моя электрнная почта work.sergeyzaharov@gmail.com
    """
)