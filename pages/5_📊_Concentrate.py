import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Concentrate", page_icon="🧪")

st.markdown("# Concentrate calculation")
st.write(
    """Расчет соответствия отработавших растворов Гигиеническим нормативам ГН 2.1.5.1315-03 в части ПДК"""
)

pdk = pd.read_csv("pdk.csv")

st.dataframe(pdk)