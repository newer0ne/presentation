import streamlit as st
import telegram
import asyncio
import time

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

# Загрузка секретов из файла secrets.toml
#token1 = str(st.secrets["token1"])
#token2 = str(st.secrets["token2"])
chat_id = st.secrets["chat_id"]
#token = token1 + ":" + token2

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
    """
)        

async def send_telegram_message(token, chat_id, text):
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text)

@st.experimental_asyncio
async def main():
    if st.button('Предложить идею!'):
        txt = st.text_area('Напишите здесь')
        if txt:
            await send_telegram_message("6328980463:AAFleAoJqyk9MBX3zU-TNQG4656DWWOIluI", chat_id, txt)
            st.write('Ваша идея отправлена!')
        else:
            st.error('Пожалуйста, введите текст сообщения')

asyncio.run(main())

st.markdown(
    """    
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