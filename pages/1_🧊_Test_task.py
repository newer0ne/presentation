import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Test task",
    page_icon="🧊",
)

header_tasklink = """[<h2 style='text-align: center;'>Test task</h2>](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)"""
st.markdown(header_tasklink, unsafe_allow_html=True)

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

image = Image.open('images/relationships.png')
st.image(image, caption='Relationships of the tables')

st.markdown(
    """
    ### Атрибуция лид - покупка
    
    Каждому лиду “в зачет” идут только те покупки, которые клиент сделал в первые 15
    дней после создания заявки. Из-за особенности бизнеса соотношение
    лидов и продаж - многие ко многим. Существующий клиент может купить услугу 
    повторно через заведение новой заявки, а может создать две заявки подряд 
    и после этого сделать покупку.
"""
)

with st.expander('Чтобы однозначно атрибутировать продажи к лидам здесь лежат примеры:'):
    st.write(
        """
        1. У клиента несколько лидов подряд, а затем продажа. 
        Продажа засчитывается последнему лиду, который был создан не позже, чем 15 дней до.
        """
        )

    mindmap = Image.open('images/Mind_Map.jpg')
    st.image(mindmap, caption='1. Продажа засчитывается последнему лиду')

    st.write(
        """
        2. У клиента несколько лидов подряд, а затем продажа. 
        Продажа не засчитывается ни одному лиду, 
        тк была создана позже 15 дней после последнего лида.
        """
        )

    mindmap1 = Image.open('images/Mind_Map_(1).jpg')
    st.image(mindmap1, caption='2. Продажа не засчитывается за окном в 15 дней')

    st.write(
        """
        3. У клиента несколько лидов подряд, а затем продажа. 
        Продажа засчитывается последнему лиду, 
        который был создан не позже, чем 15 дней до. 
        """
        )

    mindmap2 = Image.open('images/Mind_Map_(2).jpg')
    st.image(mindmap2, caption='3. Продажа засчитывается лиду не позже, чем 15 дней до')

    st.write(
        """
        4. У клиента несколько лидов и продаж вперемешку. 
        Каждая продажа засчитывается ближайшему по времени лиду.
        """
        )

    mindmap3 = Image.open('images/Mind_Map_(3).jpg')
    st.image(mindmap3, caption='4. Продажа засчитывается ближайшему по времени лиду')

st.markdown(
    """
    ### Обратите внимание
    
    - Постарайтесь не использовать циклы, если вы пишете на pandas. В 99% случаев они вам не нужны.
    - В данных могут быть дубли, а также логические несоответствия. 
        В случае выявления подобного - очистите данные по своему усмотрению и укажите это в Комментарии.
    - Не для каждого рекламного показа может быть заведена заявка, даже если деньги на нее потрачены.
    - Оформляйте код так, чтобы его было легко читать, масштабировать и переиспользовать (ООП).

    ### 2. Дополнительные задания

    - [ ]  Вывести результат в Looker Studio. В этом случае метрики CPL и ROAS создайте в виде вычисляемых полей.
    - Для референса можно использовать:
"""
)

with st.expander('Пример отчета на Looker Studio'):

    example = Image.open('images/example.png')
    st.image(example, caption='Пример отчета на Looker Studio')

st.markdown(
    """
    - [ ]  Покрыть пайплайн тестами и проверками на Data quality.

    - [ ]  Поднять БД PostgreSQL, залить сырые данные и построить пайплайн так, чтобы читать и записывать данные из/в БД.

    ### Итоговый результат

1. Готовый отчет необходимо выгрузить в Google Spreadsheet и предоставить ссылку на него. 
    
    **Набор полей в отчете**:
    
      **Dimensions**

    - Дата
    - UTM source
    - UTM medium
    - UTM campaign
        
      **Metrics**
        
    - Количество кликов
    - Расходы на рекламу
    - Количество лидов
    - Количество покупок
    - Выручка от продаж
    - CPL  - Расходы/Количество лидов
    - ROAS - Выручка/Расходы

2. Код построения пайплайна необходимо выгрузить в Git репозиторий в виде .py файла и предоставить ссылку на репозиторий. Вы можете приложить решение в notebook, но это опционально. 

3. Результат по дополнительным заданиям (опционально): 
    - Приложите ссылку на отчет в Data Looker
    - Опишите, какие проверки интегрировали в скрипт
    - Приложите скрины из БД PostgreSQL с select запросами к сырым данным и отчету (4 скрина)

    Результат отправлять [сюда](https://airtable.com/shrYDc5iUeIVLhFPu)
    """
)