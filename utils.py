import streamlit as st
import time

import sys
from datetime import datetime
import requests
import json
sys.path.append(".")  # Add the current directory to the import path
from testbed_config import TestbedTaskType, WorkCell, AMR, TaskStatus

rest_api_base_url = "http://192.168.0.46:8000"

def amr_departure_countdown(time_s):
    progress_text = "AMR is departing in " + str(time_s) + " seconds. Please stay clear of the AMR!"
    my_bar = st.progress(0, text=progress_text)
    for time_elapsed in range(time_s):
        time.sleep(1)
        time_elapsed += 1
        my_bar.progress(time_elapsed/time_s, text=progress_text)
    my_bar.empty()

def create_testbed_task(workcell_id, testbed_task_type, assembly_type_id):
    print(f'create_testbed_task: {workcell_id.name}, {testbed_task_type.name}')
    # URL of the API endpoint to create a new TestbedTask
    url = f"{rest_api_base_url}/testbedtasks/"

    # Prepare the data payload for the POST request
    data = {
        'status': TaskStatus.ENQUEUED.value,  # Assuming status is managed as a string
        'enqueue_time': datetime.now().isoformat(),  # Current time in ISO format
        'workcell_id': workcell_id.value,
        'testbed_task_type': testbed_task_type.value,
        'assembly_type_id': assembly_type_id,
        # Leave assembly_workflow_id and material_transport_task_chain_id empty
    }

    # Send the POST request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    return response