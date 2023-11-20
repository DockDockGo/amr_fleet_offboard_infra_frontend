import streamlit as st

import stat
import sys
sys.path.append("..")  # Add the parent directory to the import path

import requests
import json

from utils import rest_api_base_url

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

def request_new_assembly(assembly_type_id):
    url = f'{rest_api_base_url}/assembly-workflows/'
    headers = {
        "Content-Type": "application/json"
    }
    data = {
      "model_assembly_type_id": assembly_type_id
    }   
    response = requests.post(url, data=json.dumps(data), headers=headers)
    st.write("Response:")
    st.json(response.json() if response.status_code == 200 else response.text)

st.title("Request New Lego Assembly")

col1, col2, col3 = st.columns(3)
with col1:
    st.image("assets/lego_M.png", width=220)
    if st.button("Enqueue Assemly of letter M", use_container_width=True):
        request_new_assembly(1)
with col2:
    st.image("assets/lego_F.png", width=220)
    if st.button("Enqueue Assemly of letter F", use_container_width=True):
        request_new_assembly(2)
with col3:
    st.image("assets/lego_I.png", width=220)
    if st.button("Enqueue Assemly of letter I", use_container_width=True):
        request_new_assembly(3)
