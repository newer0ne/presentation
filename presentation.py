import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

st.markdown(
    """

    # Привет и добро пожаловать в Datalyzer! 👋

    Datalyzer — это проект по подготовке датафреймов для сквозной
    аналитики данных и последующей их визуализации.

    ### Как это работает?
    Для работы алгоритмов нужен хороший интернет,
    и если его нет - придётся немного подождать 🥲

    ***Слева расположен сайдбар с выбором вкладок***:

    - «Test task» - тестовое задание.
    - «Test task solution» - обрабатка датафреймов из тестового задания.
    - «Plotting Demo» - рандомизированный график.
    - «DataFrame visualizer» - визуализатор датафреймов.
        Для примера взято валовое сельскохозяйственное производство по годам.

    ### Что дальше?
    - Завершение работы над «Dataizer workspase».
    - Добавление автоматического анализа А/В тестов.


    ### Хотите знать немного больше об авторе?
    - Мои работы:
        - [Классификатор для РОСАТОМА](https://classificator.streamlit.app/)
        - [Атесстация в ИТМО](https://itmofinishwork.streamlitapp.com/)
    - Здесь мои социальные сети:
        - [telegram.org](https://t.me/newer0ne)
        - [linkedin.com](https://www.linkedin.com/in/sergey-zakharov-162331223/)
        - [vk.com](https://vk.com/id1237712)
        - [github.com](https://github.com/newer0ne)
    - Контакты на рекрутинговых платформах:
        - [headhunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
        - [career.habr.com](https://career.habr.com/sergeyzaharov123)
    - Если возникли какие-то вопросы моя электрнная почта work.sergeyzaharov@gmail.com
"""
)