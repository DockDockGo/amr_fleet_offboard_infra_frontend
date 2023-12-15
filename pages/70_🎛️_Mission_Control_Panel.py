import stat
import sys
sys.path.append("..")  # Add the parent directory to the import path

import requests
import json
import datetime
import streamlit as st
import pandas as pd
import numpy as np

from utils import rest_api_base_url

from testbed_config import WorkCell, AMR, TaskStatus

SENTINEL_DOCK_ID = 100

st.set_page_config(
    page_title="Mission Control Panel",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    },
)

def fetch_all_amr_missions():
    url = f"{rest_api_base_url}/amrmissions/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def create_new_amr_mission(amr_id, goal):
    data = {
        'status': TaskStatus.ENQUEUED.value,  # Set status to ENQUEUED using integer value
        'start': SENTINEL_DOCK_ID,  # Temporarily setting this to 0 as it is not currently used on the backend
        'goal': goal.value,  # Use integer value of the enum
        'enqueue_time': datetime.datetime.now().isoformat(),  # Set enqueue time to now
        # Leave the following fields null/empty
        'amr_id': amr_id,
        'material_transport_task_chain_id': None,
        'assembly_workflow_id': None,
        'start_time': None,
        'end_time': None,
    }

    url = f"{rest_api_base_url}/amrmissions/"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    return response

amr_id_mapping = {e.value: e.name for e in AMR}
workcell_mapping = {e.value: e.name for e in WorkCell}
status_mapping = {e.value: e.name for e in TaskStatus}

# Streamlit interface
st.title("AMR Mission Control Panel")

st.markdown(f"### Mission Queue")

amr_missions_data = fetch_all_amr_missions()

# Display dashboard style metrics
if amr_missions_data:
    df = pd.DataFrame(amr_missions_data)
    df['status'] = df['status'].map(status_mapping)
    
    # Count the number of missions in RUNNING and COMPLETED status
    running_count = df[df['status'] == TaskStatus.RUNNING.name].shape[0]
    completed_count = df[df['status'] == TaskStatus.COMPLETED.name].shape[0]

    # Calculate metrics for COMPLETED missions
    completed_missions = df[df['status'] == TaskStatus.COMPLETED.name]
    if not completed_missions.empty:
        # Convert times to datetime
        completed_missions['start_time'] = pd.to_datetime(completed_missions['start_time'])
        completed_missions['end_time'] = pd.to_datetime(completed_missions['end_time'])

        # Calculate completion time in a desired time unit (e.g., seconds)
        completed_missions['completion_time'] = (completed_missions['end_time'] - completed_missions['start_time']).dt.total_seconds()

        # Calculate the average completion time
        avg_completion_time = completed_missions['completion_time'].mean()

        # Calculate the standard deviation, min, and max
        std_deviation = completed_missions['completion_time'].std()
        min_time = completed_missions['completion_time'].min()
        max_time = completed_missions['completion_time'].max()
    else:
        avg_completion_time = std_deviation = min_time = max_time = np.nan
    
    # Display the status counts in a dashboard-style
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Running Missions", value=running_count)
    with col2:
        st.metric(label="Completed Missions", value=completed_count)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Average Completion Time (seconds)", value=f"{avg_completion_time:.2f}" if not np.isnan(avg_completion_time) else "N/A")
    with col2:
        st.metric(label="Standard Deviation (seconds)", value=f"{std_deviation:.2f}" if not np.isnan(std_deviation) else "N/A")
    with col3:
        st.metric(label="Minimum Time (seconds)", value=f"{min_time:.2f}" if not np.isnan(min_time) else "N/A")
    with col4:
        st.metric(label="Maximum Time (seconds)", value=f"{max_time:.2f}" if not np.isnan(max_time) else "N/A")


st.markdown("## All Missions")
if amr_missions_data:
    df = pd.DataFrame(amr_missions_data)
    df = df.sort_values(by=['enqueue_time'], ascending=False)
    
    # Replace the integer values with enum names
    df['amr_id'] = df['amr_id'].map(amr_id_mapping)
    df['goal'] = df['goal'].map(workcell_mapping)
    df['status'] = df['status'].map(status_mapping)

    df = df[['url', 'amr_id', 'goal', 'enqueue_time', 'status']]

    # Display Table
    st.table(df)
else:
    st.write("No AMRMission data available.")

# Assuming AMR is an enum or list-like structure with all the AMRs
amr_list = list(AMR)

# Create columns for each AMR
cols = st.columns(len(amr_list))

for i, amr in enumerate(amr_list):
    with cols[i]:
        st.markdown(f"## Command {amr.name} individually")
        for goal in WorkCell:
            if goal == WorkCell.UNDEFINED or goal == WorkCell.STAY_WHERE_IT_IS:
                continue
            # Creating a unique label for each button
            button_label = f"Send {amr.name} to {goal.name}"

            if st.button(button_label, key=f"{amr.name}_{goal.name}", use_container_width=True):
                response = create_new_amr_mission(amr.value, goal)
                # Displaying the response from the API call
                st.write("Response:")
                st.json(response.json() if response.status_code == 200 else response.text)
    
    # Add a divider after each AMR's column
    if i < len(amr_list) - 1:
        st.divider()

# Assuming AMR is an enum or list-like structure with all the AMRs
amr_list = list(AMR)

def execute_amr_missions(selected_AMR_1_goal, selected_AMR_2_goal):
    # Fetch all AMR missions
    missions = fetch_all_amr_missions()
    
    # Check if any mission is currently running
    if any(mission['status'] == TaskStatus.RUNNING.value for mission in missions):
        st.error("Cannot enqueue new missions while existing missions are still running")
        return

    # If no running missions, enqueue new missions for AMR_1 and AMR_2
    response_AMR_1 = create_new_amr_mission(AMR.AMR_1.value, selected_AMR_1_goal)
    response_AMR_2 = create_new_amr_mission(AMR.AMR_2.value, selected_AMR_2_goal)

    # You can handle the responses as needed, for example:
    st.success(f"New mission for AMR_1 created with response: {response_AMR_1.json()}")
    st.success(f"New mission for AMR_2 created with response: {response_AMR_2.json()}")


st.markdown("## Control both AMRs at once.")

# Create FVD Controls that allow the instructors to command one or each of the robots to goals
disallowed_goals = [WorkCell.UNDEFINED]
goal_options = {work_cell.name: work_cell.value for work_cell in WorkCell if work_cell not in disallowed_goals}
col1, col2 = st.columns(2)
with col1:
    amr = AMR.AMR_1
    selected_option = st.selectbox(f"Select where you would like to command {amr.name} to go.",
                 options=goal_options.keys(), index=list(goal_options.keys()).index("STAY_WHERE_IT_IS"))
    selected_AMR_1_goal = goal_options[selected_option]
with col2:
    amr = AMR.AMR_2
    selected_option = st.selectbox(f"Select where you would like to command {amr.name} to go.",
                 options=goal_options.keys(), index=list(goal_options.keys()).index("STAY_WHERE_IT_IS"))
    selected_AMR_2_goal = goal_options[selected_option]
if st.button("Send commands", key="send_fleet_commands", use_container_width=True):
    execute_amr_missions(WorkCell(selected_AMR_1_goal), WorkCell(selected_AMR_2_goal))

st.markdown("## Manual controls")

def create_fvd_fleet_button(goal1, goal2):
    button_label = f"Send {AMR.RICK.name} to {goal1.name}, {AMR.MORTY.name} to {goal2.name}"
    if st.button(button_label, key=f"{AMR.RICK.name}_{goal1.name}_{AMR.MORTY.name}_{goal2.name}", use_container_width=True):
        # Command RICK
        response = create_new_amr_mission(AMR.RICK.value, goal1)
        # Displaying the response from the API call
        st.write("Response:")
        st.json(response.json() if response.status_code == 200 else response.text)
        # Command MORTY
        response = create_new_amr_mission(AMR.MORTY.value, goal2)
        # Displaying the response from the API call
        st.write("Response:")
        st.json(response.json() if response.status_code == 200 else response.text)

def update_testbedtask_status(mission_url, new_status=TaskStatus.CANCELED):
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
    # if response.status_code != 200:
    #     raise Exception(f'Error occurred while updating AMRMission: {response.text}')
    
    # Return the response JSON if needed
    return response.json()

st.markdown("### Update Mission Status to CANCELLED")
st.markdown("Note that this only updates the status of the mission in the database. It does not propagate cancellation to the AMR fleet. However, missions that were enqueued and not yet started will not be executed by the fleet.")

if amr_missions_data:
    # Filter out the missions that are not completed
    non_completed_missions = df[df['status'] != TaskStatus.COMPLETED.name]
    non_completed_missions = non_completed_missions[non_completed_missions['status'] != TaskStatus.CANCELED.name]

    # Iterate through each non-completed mission and create a button
    for index, mission in non_completed_missions.iterrows():
        mission_url = mission['url']
        mission_id = mission['amr_id']
        mission_status = mission['status']

        # Button label with mission ID and current status
        button_label = f"Cancel {mission_url} (Current: {mission_status})"

        # Create a button for each mission
        if st.button(button_label, key=f"update_{mission_url}"):
            # Call update_testbedtask_status with the mission URL
            # Assuming you want to update the status to CANCELLED as an example
            update_response = update_testbedtask_status(mission_url, TaskStatus.CANCELED)
            
            # Display the response
            st.write("Response:")
            # st.json(update_response if update_response.status_code == 200 else update_response.text)
            st.json(update_response)
else:
    st.write("No AMRMission data available.")