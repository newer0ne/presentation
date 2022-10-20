import streamlit as st

link_test_task = '[Тестовое задание](https://xoservices.notion.site/1872d331265946a0ae2c5c9069189fd7)'
st.markdown(link_test_task, unsafe_allow_html=True)

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

rows_ads = run_query(f'SELECT * FROM "{https://drive.google.com/file/d/1U7DQGPOEhGWW3aWQHZayF_9ScqBYnaE1/}"')
ads = pd.DataFrame(rows_ads, dtype=str)
st.dataframe(data = ads)