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

st.write("Display a list of available assemblies here, along with a button to queue an assembly for execution in the testbed.")
