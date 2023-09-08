import streamlit as st

st.set_page_config(
    page_title="Testbed Control Panel",
    page_icon="🎛️",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Testbed Control Panel")

st.write("Display the current finite state machine states of all active assemblies in the testbed here, along with buttons to send commands to interface with the AMR fleet API.")