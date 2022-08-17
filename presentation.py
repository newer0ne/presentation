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

st.title('Сергей Владимирович Захаров')
st.write('Мужчина, 31 год, родился 3 февраля 1991')
st.write('+79006241050 / t.me/newer0ne / work.sergeyzaharov@gmail.com')

st.header('Ведущий Инженер-конструктор')

st.header('ТИТАН-2, холдинг')
