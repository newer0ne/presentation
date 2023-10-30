import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.markdown("<h1 style='text-align: center;'>Привет и добро пожаловать! 👋</h1>", unsafe_allow_html=True)

st.markdown(
    """
    Рад приветствовать Вас на странице моих проектов.
    Каждая страница слева реализована под конкретную прикладную задачу.

    ### Как это работает?
    Для работы алгоритмов нужен хороший интернет,
    и если его нет - придётся немного подождать 🥲

    ### Слева расположен сайдбар с выбором вкладок:
    - «EPP calculation» - Калькулятор режимов электролитно-плазменного полирования.
    - «Concentrate» - Калькулятор ПДК отработавших растворов электролита.
    - «АВ Tester» - Анализ результатов A/B теста с графическим отображением
        результата и вычислением основных параметров.    
    - «ADS analyzer» - обрабатка датафреймов для сквозной аналитики продажи-лиды-покупки.
    - «DataFrame visualizer» - визуализатор датафреймов.
        Для примера взято валовое сельскохозяйственное производство по годам.

    ### Что дальше?
    - «ADS analyzer»: 
        расширение функционала модуля загрузок, внутренний управляемый ренейм колонок.
    - «DataFrame visualizer»:
        Добавление выбора стандартных баз данных для отображения.
        Добавление drag&drop просмотра данных.
    """
)        

st.markdown(
    """    
        ## Об авторе 
    - Cоциальные сети:
        - [telegram.org](https://t.me/newer0ne)
        - [linkedin.com](https://www.linkedin.com/in/zakharovsv/)
        - [vk.com](https://vk.com/id1237712)
        - [github.com](https://github.com/newer0ne)
    - Рекрутинговые платформы:
        - [headhunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
        - [career.habr.com](https://career.habr.com/sergeyzaharov123)
    - Если возникли какие-то вопросы - моя электрнная почта work.sergeyzaharov@gmail.com
    """
)