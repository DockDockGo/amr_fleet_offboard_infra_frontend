import streamlit as st
import sys
sys.path.append("..")  # Add the parent directory to the import path
from utils import amr_departure_countdown

st.set_page_config(
    page_title="Assembly WorkCell 01",
    page_icon="🦾",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Assembly Work Cell 01 HRI")

st.write("Provide assembly instructions to the human operator here. Sample:")
st.image(
    [
        "assets/sample_building_instructions/01.png",
        "assets/sample_building_instructions/02.png",
        "assets/sample_building_instructions/03.png",
        "assets/sample_building_instructions/04.png",
        "assets/sample_building_instructions/05.png",
    ]
)

# Create buttons for each step
col1, col2, col3 = st.columns(3)
if col1.button("Picked up kit from the AMR", use_container_width=True):
    st.success("The AMR will now depart to service other tasks. Please stay clear of the AMR.")
    amr_departure_countdown(5)
if col2.button("Assembled the model", use_container_width=True):
    st.success("Requested an AMR to come pick up the assembled model.")
if col3.button("Placed the assembled model on an AMR", use_container_width=True):
    st.success("The AMR will now transport the assembled model to the next work cell. Please stay clear of the AMR.")
    amr_departure_countdown(5)

