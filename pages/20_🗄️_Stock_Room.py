import streamlit as st

import sys
sys.path.append("..")  # Add the parent directory to the import path
# from utils import amr_departure_countdown

import requests
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import time

import base64

from utils import rest_api_base_url
from testbed_config import TestbedTaskType, WorkCell, AMR, TaskStatus

# Initialize session state variables
if 'check_tasks' not in st.session_state:
    st.session_state.check_tasks = True
if 'current_task_url' not in st.session_state:
    st.session_state.current_task_url = None
if 'current_task_type' not in st.session_state:
    st.session_state.current_task_type = None

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

def get_enqueued_stockroom_tasks(workcell, only_fetch_first_enqueued=True):
    enqueued_status = TaskStatus.ENQUEUED.value

    url = (f'{rest_api_base_url}/testbedtasks/?status={enqueued_status}&workcell_id={workcell.value}&ordering=enqueue_time')
    response = requests.get(url)
    print(f'response.json(): {response.json()}')

    if response.status_code != 200:
        raise Exception(f'Error occurred while fetching AMRMissions: {response.text}')
    # If no enqueued tasks
    if len(response.json()) == 0:
        return None
    if only_fetch_first_enqueued:
        return response.json()[0]
    return response.json()

# Function to update the status of an AMR mission
def update_testbedtask_status(mission_url, new_status):
    # Prepare the data to be patched
    patch_data = {'status': new_status.value}
    if new_status == TaskStatus.RUNNING:
        patch_data['start_time'] = datetime.now().isoformat()
    if new_status == TaskStatus.COMPLETED:
        patch_data['end_time'] = datetime.now().isoformat()

    print(f'mission_url: {mission_url}, patch_data: {patch_data}')

    # Send the PATCH request
    response = requests.patch(mission_url, json=patch_data)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f'Error occurred while updating AMRMission: {response.text}')
    
    # Return the response JSON if needed
    return response.json()
    
def create_testbed_task(workcell_id, testbed_task_type):
    print(f'create_testbed_task: {workcell_id.name}, {testbed_task_type.name}')
    # URL of the API endpoint to create a new TestbedTask
    url = f"{rest_api_base_url}/testbedtasks/"

    # Prepare the data payload for the POST request
    data = {
        'status': TaskStatus.ENQUEUED.value,  # Assuming status is managed as a string
        'enqueue_time': datetime.now().isoformat(),  # Current time in ISO format
        'workcell_id': workcell_id.value,
        'testbed_task_type': testbed_task_type.value,
        # Leave assembly_workflow_id and material_transport_task_chain_id empty
    }

    # Send the POST request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    return response

def fetch_tasks():
    task = get_enqueued_stockroom_tasks(WorkCell.STOCK_ROOM)
    if task is not None:
        st.session_state.current_task_url = task['url']
        # st.write(f'st.session_state.current_task_url: {st.session_state.current_task_url}')
        st.session_state.current_task_type = task['testbed_task_type']
        # st.write(f'st.session_state.current_task_type: {st.session_state.current_task_type}')
        st.session_state.check_tasks = False
        update_testbedtask_status(st.session_state.current_task_url, TaskStatus.RUNNING)

def complete_task():
    update_testbedtask_status(st.session_state.current_task_url, TaskStatus.COMPLETED)
    
    if st.session_state.current_task_type == TestbedTaskType.UNLOADING.value:
        create_testbed_task(WorkCell.STOCK_ROOM, TestbedTaskType.PROCESSING)
    
    st.session_state.check_tasks = True
    st.session_state.current_task_url = None
    st.session_state.current_task_type = None

    st.experimental_rerun()

def manage_task_polling():
    # Function to manage task polling
    if st.session_state.check_tasks:
        st.write("Polling for new tasks, no action needed at the moment!")
        fetch_tasks()
        # Schedule a rerun after 5 seconds
        st.session_state.rerun_in = time.time() + 0.5

def schedule_rerun():
    # Function to schedule a rerun
    if 'rerun_in' in st.session_state and time.time() > st.session_state.rerun_in:
        del st.session_state.rerun_in
        st.experimental_rerun()

################## GUI LAYOUT ##################

st.title("Stock Room HRI")

# Display button if a task is found
# st.write(f'st.session_state.current_task_type: {st.session_state.current_task_type}')
if st.session_state.current_task_type is not None:
    if st.session_state.current_task_type == TestbedTaskType.UNLOADING.value:
        st.markdown("#### Please unload the payload from the top surface of the AMR.")
        # Hack to display gif
        file_ = open("assets/payload_unloading.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="720">',
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("I've unloaded the payload from the AMR", use_container_width=True):
            complete_task()
    elif st.session_state.current_task_type == TestbedTaskType.PROCESSING.value:
        st.write("Display instructions about which parts bins to load onto the AMR")
        if st.button("I've fetched the required parts bins", use_container_width=True):
            complete_task()
    elif st.session_state.current_task_type == TestbedTaskType.LOADING.value:
        # st.image("assets/payload_loading.gif", use_container_width=True)
        st.markdown("#### Please load the payload from the top surface of the AMR.")
        # Hack to display gif
        file_ = open("assets/payload_loading.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif2" width="720">',
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("I've loaded the payload onto the AMR", use_container_width=True):
            complete_task()
else:
    # Task checking loop
    if st.session_state.check_tasks:
        st.write("Polling for new tasks, no action needed at the moment!")
        fetch_tasks()
        # Sleep for 1 second before next check
        time.sleep(5)
        # Trigger a rerun of the app
        st.experimental_rerun()

# # Task checking loop
# if st.session_state.check_tasks:
#     st.write("Polling for new tasks, no action needed at the moment!")
#     fetch_tasks()
#     # Sleep for 1 second before next check
#     time.sleep(5)
#     # Trigger a rerun of the app
#     st.experimental_rerun()

# # Manage task polling
# manage_task_polling()

# # Schedule a rerun if needed
# schedule_rerun()

# # Display button if a task is found
# st.write(f'st.session_state.current_task_type: {st.session_state.current_task_type}')
# if st.session_state.current_task_type == TestbedTaskType.UNLOADING.value:
#     # st.image("assets/payload_unloading.gif", use_column_width=True)
#     if st.button("I've unloaded the payload from the AMR", use_container_width=True):
#         complete_task()
# elif st.session_state.current_task_type == TestbedTaskType.PROCESSING.value:
#     st.write("Display instructions about which parts bins to load onto the AMR")
#     if st.button("I've fetched the required parts bins", use_container_width=True):
#         complete_task()
# elif st.session_state.current_task_type == TestbedTaskType.LOADING.value:
#     # st.image("assets/payload_loading.gif", use_column_width=True)
#     if st.button("I've loaded the payload onto the AMR", use_container_width=True):
#         complete_task()