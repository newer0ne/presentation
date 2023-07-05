import streamlit as st
import pandas as pd
import chardet

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

pdk = "pdk.xlsx"

with open(f'{pdk}', 'rb') as f:
    result = chardet.detect(f.read())
    
# Чтение файла с определенной кодировкой
df = pd.read_excel(pdk)#, encoding=result['encoding'])

st.dataframe(df)
