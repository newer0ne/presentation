import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

header_tasklink = "[<h2 style='text-align: center;'>Привет и добро пожаловать в Datalyzer! 👋</h2>]"""
st.markdown(header_tasklink, unsafe_allow_html=True)

st.markdown(
    """
    Datalyzer — это проект по подготовке датафреймов для сквозной
    аналитики данных и последующей их визуализации. Проект разрабатывался
    по тестовому заданию XO ANALYTICS.
    
    ### Как это работает?
    ⬅️ Слева расположен сайдбар с выбором вкладок.
    На вкладке «Test task» расположено тестовое задание.
    Датафреймы обрабатываются на вкладке «Dataizer workspase»

    ### Что дальше?
    - Расширение функционала обработки датафреймов
    - Визуализация полученных промежуточных и конечных результатов,
        предполагается адаптировать «Plotting Demo».


    ### Хотите знать немного больше об авторе?
    - Мой проект для РОСАТОМА:
        - [Классификатор](https://classificator.streamlit.app/)
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