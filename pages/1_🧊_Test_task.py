import streamlit as st
from PIL import Image

st.header('Тестовое задание')

st.subheader('1. Основное задание')

st.markdown(
    """
    ### 1. Основное задание
    В данной задаче в рамках тестового задания необходимо построить сквозную аналитику для салона красоты. 
    У салона есть реклама в онлайне и сайт, через который можно оставить заявку на услугу. 
    При помощи сквозной аналитики нужно проследить путь от клика по рекламному объявлению до покупки и, таким образом, оценить эффективность маркетинга. 
    Клик по рекламе трансформируется в лид (заявку), а лид превращается в клиента, который уже может совершить некоторое количество покупок.
    Необходимо подготовить данные для отчета по сквозной аналитике. Для решения можно использовать на выбор: SQL или Python (Pandas).
    Данные поступают на вход в виде 3 csv файлов:
        - ads.csv
        - leads.csv
        - purchases.csv

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