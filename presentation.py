import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Datalyzer! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Datalyzer is a project for preparing dataframes for end-to-end 
    data analytics and subsequent visualization.
    

    ### Want to know more about the author?
    - Сheck my social media 
        [telegramm.org](https://t.me/newer0ne)
        & [vk.com](https://vk.com/id1237712)
    - Or pages on recruiting platforms 
        [headHunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75) 
        & [career.habr.com](https://career.habr.com/sergeyzaharov123)

    - Ask any other question by email [email](work.sergeyzaharov@gmail.com)

"""
)