import streamlit as st
from st_pages import Page, show_pages

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# show_pages(
#     [
#         Page('main_page.py', 'Главная'),
#         Page('pages/1_epp_calculation.py', 'Рассчет режимов ЭПП'),
#         Page('pages/2_concentrate.py', 'Рассчет ПДК растворов')
#     ]
# )


st.markdown(("<h1 style='text-align: center;'>Привет и добро пожаловать! "
             "👋</h1>"), unsafe_allow_html=True)

st.markdown("""Рад приветствовать Вас на странице моих проектов.
            Каждая страница создана под конкретную задачу.
            Со временем функционал будет расширяться 📈
            """)

st.markdown("### Проекты:")

# Задаем ширину и высоту контейнеров в пикселях
container_style = """width: 300px;
                height: 300px;
                border: 1px solid black;
                padding: 10px;"""

with st.container(border=True):
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.image('pictures/EPP_calculation.png')
    with col1_2:
        st.markdown(
            "### [EPP calculation](http://sergeyzaharov.ru/epp_calculation)")
        st.write(
            'Калькулятор режимов электролитно-плазменного полирования')

with st.container(border=True):
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.image('pictures/Concentrate.png')
    with col2_2:
        st.markdown(
            "### [Concentrate](http://sergeyzaharov.ru/concentrate)")
        st.write(
            'Калькулятор ПДК отработавших растворов электролита')

with st.container(border=True):
    st.markdown(
        """
            ## Об авторе
        """
        )
    col5_1, col5_2 = st.columns(2)
    with col5_1:
        st.markdown("""
- Cоциальные сети:
    - [telegram.org](https://t.me/newer0ne)
    - [linkedin.com](https://www.linkedin.com/in/zakharovsv/)
    - [vk.com](https://vk.com/id1237712)
    - [github.com](https://github.com/newer0ne)
                    """)
    with col5_2:
        st.markdown(
            """
- Рекрутинговые платформы:
    - [hh.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
    - [career.habr.com](https://career.habr.com/sergeyzaharov123)
- Если возникли какие-то вопросы:
    - моя электрнная почта work.sergeyzaharov@gmail.com
            """)
