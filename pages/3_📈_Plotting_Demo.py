import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """Эта развлекательная демонстрация иллюстрирует комбинацию
    построения графиков и анимации. Нужно выбрать скорость
    отрисовки, а генератор случайных чисел в течении 
    нескольких секунд будет регенерировать график.
    Для повторной генерации просто нажми "Сначала!".
    - **Заставь его рисовать графики!**"""
)

timelag = [2, 5, 10]
Sleeptime = st.radio(
        "Сколько секунд отрисовывать график?",
        (timelag))

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(Sleeptime/100)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Сначала!")