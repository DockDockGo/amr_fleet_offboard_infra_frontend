import streamlit as st

st.set_page_config(
    page_title="Kitting Station",
    page_icon="🍱",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Kitting Station HRI")

st.markdown(
    """
    Display task instructions for how to compile kits for the requested lego assemblies here.
    This will involve 4 steps:
    1. Picking up the bins transported by an AMR from the stock room.
    2. Assembling the kit using parts from the supplied bins.
    3. Placing the assembled kit on an AMR for transport to the next work cell.
    4. Placing the empty bins on an AMR for transport back to the stock room.
    """
)

# Create buttons for each step
col1, col2, col3, col4 = st.columns(4)
if col1.button("Picked up the bins from the AMR", use_container_width=True):
    st.success("The AMR will now depart to service other tasks. Please stay clear of the AMR!")
if col2.button("Assembled the kit", use_container_width=True):
    st.success("Requested an AMR to come pick up the assembled model.!")
if col3.button("Placed the assembled kit on an AMR", use_container_width=True):
    st.success("The AMR will now transport the assembled kit to an assembly work cell. Please stay clear of the AMR!")
if col4.button("Placed the parts bins back on an AMR", use_container_width=True):
    st.success("The AMR will now transport the parts bins to the stock room. Please stay clear of the AMR!")




