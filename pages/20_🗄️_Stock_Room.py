import streamlit as st

import sys
sys.path.append("..")  # Add the parent directory to the import path
# from utils import amr_departure_countdown

import requests
import json
import datetime
import streamlit as st
import pandas as pd
import numpy as np

from utils import rest_api_base_url

from testbed_config import WorkCell, AMR, TaskStatus

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

def fetch_all_testbed_tasks():
    url = f"{rest_api_base_url}/testbedtasks/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    

def create_testbed_task(workcell_id):
    """
    Creates a new TestbedTask with status set to ENQUEUED and enqueue_time set to the current time.

    :param workcell_id: The ID of the workcell for the TestbedTask.
    """
    # URL of the API endpoint to create a new TestbedTask
    url = 'http://example.com/api/testbedtasks/'  # Replace with the actual endpoint

    # Prepare the data payload for the POST request
    data = {
        'status': 'ENQUEUED',  # Assuming status is managed as a string
        'enqueue_time': datetime.now().isoformat(),  # Current time in ISO format
        'workcell_id': workcell_id,
        # Leave assembly_workflow_id and material_transport_task_chain_id empty
    }

    # Send the POST request
    response = requests.post(url, json=data)

################## GUI LAYOUT ##################

st.title("Stock Room HRI")





# st.write("Display task instructions for which bins to pick from the stock room and place on the AMR when it arrives here. Else instructions on picking up the parts bins returned from the kitting station by an AMR.")
# col1, col2 = st.columns(2)
# if col1.button("Placed parts bins on the AMR", use_container_width=True):
#     st.success("The AMR will now transport the parts bins to the kitting station. Please stay clear of the AMR!", icon="✅")
#     amr_departure_countdown(5)
# if col2.button("Picked up returned parts bins from the AMR", use_container_width=True):
#     st.success("The AMR will now depart to service other tasks. Please stay clear of the AMR!", icon="✅")
#     amr_departure_countdown(5)

