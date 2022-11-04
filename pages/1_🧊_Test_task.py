import streamlit as st
from PIL import Image

st.markdown("<h2 style='text-align: center;'>Test task</h2>", unsafe_allow_html=True)

st.markdown(
    """
    ### 1. Основное задание
    В данной задаче в рамках тестового задания необходимо построить сквозную аналитику для салона красоты. 
    У салона есть реклама в онлайне и сайт, через который можно оставить заявку на услугу. 
    При помощи сквозной аналитики нужно проследить путь от клика по рекламному объявлению до покупки и, таким образом, оценить эффективность маркетинга. 
    Клик по рекламе трансформируется в лид (заявку), а лид превращается в клиента, который уже может совершить некоторое количество покупок.
    Необходимо подготовить данные для отчета по сквозной аналитике. Для решения можно использовать на выбор: SQL или Python (Pandas).
    Данные поступают на вход в виде 3 csv файлов:

    - [ads.csv](https://drive.google.com/file/d/1PB2h2484kvv-_7skmE0hrzoaGOKXYtt9/view?usp=share_link)
    - [leads.csv](https://drive.google.com/file/d/1abKQREXlfSpM8FIUu6gHC2cYCaF1DBgQ/view?usp=share_link)
    - [purchases.csv](https://drive.google.com/file/d/1S1NQwiwq02iFYLb2riuP4H5jCq38PkYu/view?usp=share_link)

    ### Связи

    Связь между рекламой и заявкой определяется через utm метки - 
    если набор меток из рекламного объявления совпадает с тем набором, 
    который есть в заявке, то мы можем определить сколько денег было 
    трачено на привлечение этого лида.

    Связь между лидом и продажами определяется через client_id.
"""
)

image = Image.open('relationships.png')
st.image(image, caption='Relationships og the tables')