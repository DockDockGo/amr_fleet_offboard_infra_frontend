import streamlit as st

import sys
sys.path.append("..")  # Add the parent directory to the import path
from utils import amr_departure_countdown

st.set_page_config(
    page_title="Stock Room",
    page_icon="🗄️",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Stock Room HRI")

st.write("Display task instructions for which bins to pick from the stock room and place on the AMR when it arrives here. Else instructions on picking up the parts bins returned from the kitting station by an AMR.")

col1, col2 = st.columns(2)
if col1.button("Places parts bins on the AMR", use_container_width=True):
    st.success("The AMR will now transport the parts bins to the kitting station. Please stay clear of the AMR!", icon="✅")
    amr_departure_countdown(5)
if col2.button("Picked up returned parts bins from the AMR", use_container_width=True):
    st.success("The AMR will now depart to service other tasks. Please stay clear of the AMR!", icon="✅")
    amr_departure_countdown(5)

