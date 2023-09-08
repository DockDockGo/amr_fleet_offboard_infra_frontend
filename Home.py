import streamlit as st

st.set_page_config(
    page_title="Testbed Control Panel",
    page_icon="🏠",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Welcome to MFI's Lego Assembly Testbed Simulator!")

st.image("assets/testbed_amr_role.gif")

st.markdown(
    """
    This webapp serves as a stand-in replacement for the fully automated lego assembly testbed in development at Carnegie Mellon University's Manufacturing Futures Institute.
    
    Its purpose is two-fold:
    1. To **emulate the commands that will be sent to the testbed's transportation layer**: a fleet of automated mobile robots (AMRs) developed by a team of student roboticists from the Robotics Institute at CMU
    2. Providing **user-interfaces that provide manipulation instructions to human operators** at the different work cells of the testbed. This allows for a full **demo of the testbed's transportation infrastructure capabilities using AMRs** while the automated robot arms that will later be performing the manipulation tasks are in development.
    """
    )

