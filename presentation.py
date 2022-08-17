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

st.title('Группа Автоматизации') 
st.write('Проект создания Группы Автоматизации')
st.write('в составе Отдела Инновационных Технологий')
st.write('Проектно Конструкторской Группы АО “КОНЦЕРН ТИТАН-2”')

st.header('Состав группы:')
st.write('Начальник группы - Алексеев Юрий Васильевич')
st.write('Ведущий инженер - Захаров Сергей Владимирович')
st.write('Ведущий инженер - Осатюк Валерий Сергеевич')
st.write('Ведущий инженер-расчётчик - Степанян Артур Юрьевич')


st.header('ТИТАН-2, холдинг')
