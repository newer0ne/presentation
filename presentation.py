import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="📖",
)

st.write("# Welcome to Datalyzer! 👋")

st.markdown(
    """
    Datalyzer is a project for preparing dataframes for end-to-end 
    data analytics and subsequent visualization.
    
    ### Where is what?
    On the left is a panel with a choice of workspaces. Dataframes
    are processed on the "Dataizer Workspace" tab, and the 
    "Plotting Demo" tab is selected for visualization of the
    obtained intermediate and final results.

    ### Want to know more about the author?
    - Check out another one of my projects for ROSATOM:
        - [Классификатор](https://classificator.streamlit.app/)
    - And check my social media:
        - [telegramm.org](https://t.me/newer0ne)
        - [linkedin.com](https://www.linkedin.com/in/sergey-zakharov-162331223/)
        - [vk.com](https://vk.com/id1237712)
        - [github.com](https://github.com/newer0ne)
    - Or pages on recruiting platforms:
        - [headhunter.ru](https://hh.ru/resume/7e8af31aff09d92df80039ed1f674457646c75)
        - [career.habr.com](https://career.habr.com/sergeyzaharov123)
    - Ask any other question by email work.sergeyzaharov@gmail.com

"""
)