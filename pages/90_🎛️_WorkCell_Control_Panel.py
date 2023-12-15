import stat
import sys
sys.path.append("..")  # Add the parent directory to the import path

import requests
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np

from utils import rest_api_base_url, create_testbed_task

from testbed_config import TestbedTaskType, WorkCell, AMR, TaskStatus

workcell_mapping = {e.value: e.name for e in WorkCell}
status_mapping = {e.value: e.name for e in TaskStatus}
testbedtasktype_mapping = {e.value: e.name for e in TestbedTaskType}

st.set_page_config(
    page_title="WorkCell Control Panel",
    page_icon="🎛️",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    },
)

def fetch_all_testbed_tasks():
    url = f"{rest_api_base_url}/testbedtasks/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
# def create_testbed_task(workcell_id, testbed_task_type, assembly_type_id):
#     # URL of the API endpoint to create a new TestbedTask
#     url = f"{rest_api_base_url}/testbedtasks/"

#     # Prepare the data payload for the POST request
#     data = {
#         'status': TaskStatus.ENQUEUED.value,  # Assuming status is managed as a string
#         'enqueue_time': datetime.now().isoformat(),  # Current time in ISO format
#         'workcell_id': workcell_id.value,
#         'testbed_task_type': testbed_task_type.value,
#         'assembly_type_id': assembly_type_id,
#         # Leave assembly_workflow_id and material_transport_task_chain_id empty
#     }

#     # Send the POST request
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(url, data=json.dumps(data), headers=headers)
    
#     return response

st.title("WorkCell Control Panel")

st.markdown(f"### TestbedTask Queue")

testbed_task_data = fetch_all_testbed_tasks()

if testbed_task_data:
    df = pd.DataFrame(testbed_task_data)
    df['status'] = df['status'].map(status_mapping)
    df['workcell_id'] = df['status'].map(workcell_mapping)

    # Count the number of missions in RUNNING and COMPLETED status
    running_count = df[df['status'] == TaskStatus.RUNNING.name].shape[0]
    completed_count = df[df['status'] == TaskStatus.COMPLETED.name].shape[0]

    # Display the status counts in a dashboard-style
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Running Testbed Tasks", value=running_count)
    with col2:
        st.metric(label="Completed Testbed Tasks", value=completed_count)

if testbed_task_data:
    df = pd.DataFrame(testbed_task_data)
    df = df.sort_values(by=['enqueue_time'], ascending=False)
    
    # Replace the integer values with enum names
    df['status'] = df['status'].map(status_mapping)
    df['workcell_id'] = df['status'].map(workcell_mapping)
    df['testbed_task_type'] = df['testbed_task_type'].map(testbedtasktype_mapping)

    df = df[['url', 'workcell_id', 'testbed_task_type', 'status']]

    # Display Table
    st.dataframe(df)
else:
    st.write("No AMRMission data available.")


################## GUI LAYOUT ##################

testbedtasktype_list = list(TestbedTaskType)

st.markdown("## WorkCell Task Dispatcher")

assembly_type_id = int(st.number_input("Assembly type ID", value=1))

# Create columns for each AMR
cols = st.columns(len(testbedtasktype_list))
for i, testbedtasktype in enumerate(testbedtasktype_list):
    with cols[i]:
        st.markdown(f"## {testbedtasktype.name} Commands")
        for workcell_id in WorkCell:
            if workcell_id == WorkCell.UNDEFINED:
                continue
            # Creating a unique label for each button
            button_label = f"Enqueue {testbedtasktype.name} task at {workcell_id.name}"

            if st.button(button_label, key=f"{testbedtasktype.name}_{workcell_id.name}", use_container_width=True):
                response = create_testbed_task(workcell_id, testbedtasktype, assembly_type_id)
                # Displaying the response from the API call
                st.write("Response:")
                st.json(response.json() if response.status_code == 200 else response.text)

st.markdown("## FVD controls")
st.markdown("No init")
st.markdown("Demos")

# if st.button(button_label, key=f"{testbedtasktype.name}_{workcell_id.name}_", use_container_width=True):

# def create_workcell_button(workcell_id, testbedtasktype, button_label):
#     if st.button(button_label, key=f"{}", use_container_width=True):
#         response = create_testbed_task(workcell_id, testbedtasktype, assembly_type_id)
#         # Displaying the response from the API call
#         st.write("Response:")
#         st.json(response.json() if response.status_code == 200 else response.text)