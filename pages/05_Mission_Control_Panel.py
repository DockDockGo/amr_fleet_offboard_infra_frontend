import stat
import sys
sys.path.append("..")  # Add the parent directory to the import path

import requests
import json
import datetime
import streamlit as st
import pandas as pd

from testbed_config import WorkCell, AMR, TaskStatus

api_base_url = "http://0.0.0.0:8000"

def fetch_all_amr_missions():
    url = f"{api_base_url}/amrmissions/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def create_new_amr_mission(amr_id, goal):
    data = {
        'status': TaskStatus.ENQUEUED.value,  # Set status to ENQUEUED using integer value
        'start': 0,  # Temporarily setting this to 0 as it is not currently used on the backend
        'goal': goal.value,  # Use integer value of the enum
        'enqueue_time': datetime.datetime.now().isoformat(),  # Set enqueue time to now
        # Leave the following fields null/empty
        'amr_id': None,
        'material_transport_task_chain_id': None,
        'assembly_workflow_id': None,
        'start_time': None,
        'end_time': None,
    }

    url = f"{api_base_url}/amrmissions/"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    return response

amr_id_mapping = {e.value: e.name for e in AMR}
workcell_mapping = {e.value: e.name for e in WorkCell}
status_mapping = {e.value: e.name for e in TaskStatus}

# Streamlit interface
st.title("AMR Mission Control Panel")

amr_missions_data = fetch_all_amr_missions()
if amr_missions_data:
    df = pd.DataFrame(amr_missions_data)
    df.sort_values(by='enqueue_time', inplace=True)
    
    # Replace the integer values with enum names
    df['amr_id'] = df['amr_id'].map(amr_id_mapping)
    df['goal'] = df['goal'].map(workcell_mapping)
    df['status'] = df['status'].map(status_mapping)

    df = df[['url', 'amr_id', 'goal', 'enqueue_time', 'status']]
    st.table(df)
else:
    st.write("No AMRMission data available.")

for amr in AMR:
    st.markdown(f"## {amr.name} Commands")
    for goal in WorkCell:
        if goal == WorkCell.UNDEFINED:
            continue
        # Creating a unique label for each button
        button_label = f"Send {amr.name} to {goal.name}"

        if st.button(button_label):
            response = create_new_amr_mission(amr.value, goal)
            # Displaying the response from the API call
            st.write("Response:")
            st.json(response.json() if response.status_code == 200 else response.text)
    
    st.divider()