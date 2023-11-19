import streamlit as st

st.set_page_config(
    page_title="Testbed Control Panel",
    page_icon="🧱",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Request New Lego Assembly")

st.write("Add images of lego models here")

st.button("Enqueue Assemly of letter M", use_container_width=True)
st.button("Enqueue Assemly of letter F", use_container_width=True)
st.button("Enqueue Assemly of letter I", use_container_width=True)
