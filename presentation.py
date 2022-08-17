import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import openpyxl
import io
from io import BytesIO
import os
import csv
from pyxlsb import open_workbook as open_xlsb
import webbrowser

# Отображаемый заголовок страницы ##########################################################################################################################################################

st.title('Проект создания Группы Автоматизации') 
st.write('в составе Отдела Инновационных Технологий Проектно Конструкторской Группы АО “КОНЦЕРН ТИТАН-2”')

st.header('Состав группы:')
st.write('''Начальник группы - Алексеев Юрий Васильевич
Ведущий инженер - Захаров Сергей Владимирович
Ведущий инженер - Осатюк Валерий Сергеевич
Ведущий инженер-расчётчик - Степанян Артур Юрьевич''')


st.header('ТИТАН-2, холдинг')
