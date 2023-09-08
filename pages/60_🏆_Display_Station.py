import streamlit as st

st.set_page_config(
    page_title="Display Station",
    page_icon="🏆",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Display Station HRI")

st.header("Congratulations on your newly assembled Lego Model!")

st.write("Please place it on the display stand for the final inspection.")