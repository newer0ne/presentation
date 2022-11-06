import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

st.write("# Привет и добро пожаловать в Datalyzer! 👋")

st.markdown(
    """
    Datalyzer — это проект по подготовке датафреймов для сквозной
    аналитики данных и последующей их визуализации. Проект разрабатывался
    по тестовому заданию XO ANALYTICS.
    
    ### Как это работает?
    Слева расположен сайдбар с выбором рабочих мест. 
    Датафреймы обрабатываются на вкладке «Рабочее пространство Dataizer», а для визуализации полученных промежуточных и конечных результатов выбирается вкладка «Plotting Demo».

    ### Want to know more about the author?
    - Check out another one project for ROSATOM:
        - [Классификатор](https://classificator.streamlit.app/)
    - And check my social media:
        - [telegram.org](https://t.me/newer0ne)
        - [linkedin.com](https://www.linkedin.com/in/sergey-zakharov-162331223/)
        - [vk.com](https://vk.com/id1237712)
        - [github.com](https://github.com/newer0ne)
    - Or pages on recruiting platforms:
        - [headhunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
        - [career.habr.com](https://career.habr.com/sergeyzaharov123)
    - Ask any other question by email work.sergeyzaharov@gmail.com
"""
)