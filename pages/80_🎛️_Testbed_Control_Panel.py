from pty import spawn
import stat
import sys

sys.path.append("..")  # Add the parent directory to the import path

import streamlit as st
import os
import django
from pathlib import Path
import sys
import pandas as pd

from testbed_config import WorkCell, AMR, TaskStatus, AssemblyType

# Path to the directory of your Django project
django_project_path = "/Users/sid/courses/Project/offboard_infra/testbed_emulator_backend/testbed_emulator_backend"
sys.path.insert(0, django_project_path)

# Django project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testbed_emulator_backend.settings")

# Set up Django
django.setup()

from testbed_emulator_backend_app.models import *  # Replace 'yourapp' with the name of your Django app

st.set_page_config(
    page_title="Testbed Control Panel",
    page_icon="🎛️",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    },
)

amr_id_mapping = {e.value: e.name for e in AMR}
workcell_mapping = {e.value: e.name for e in WorkCell}


def fetch_assembly_workflows():
    workflows = AssemblyWorkflow.objects.all()

    data = []

    for wf in workflows:
        workflow_data = {
            "ID": wf.id,
            "Status": wf.status_dict,  # Assuming you have a status field or method
            "Model Assembly Type ID": wf.model_assembly_type_id,
            # Include other fields as needed
        }
        data.append(workflow_data)

    return pd.DataFrame(data)


def delete_all_assembly_workflows():
    try:
        # Delete instances of models referencing TestbedTask and AMRMission
        AssemblyWorkflow.objects.all().delete()
        MaterialTransportTaskChain.objects.all().delete()

        # Now safe to delete TestbedTask and AMRMission
        TestbedTask.objects.all().delete()
        AMRMission.objects.all().delete()

        # Delete remaining models
        WorkCellState.objects.all().delete()
        AMRState.objects.all().delete()

        st.success("All data has been deleted from the database")

    except Exception as e:
        st.error(f"Error occurred: {e}")


def display_amr_states():
    # Query all AMRState objects
    amr_states = AMRState.objects.all()

    # Prepare data for display
    data = []
    for state in amr_states:
        amr_id = state.amr_id
        active_mission = state.active_mission if state.active_mission else "None"
        active_material_transport_task_chain = (
            state.active_material_transport_task_chain
            if state.active_material_transport_task_chain
            else "None"
        )
        data.append(
            {
                "amr_id": amr_id,
                "active_mission": active_mission,
                "active_material_transport_task_chain": active_material_transport_task_chain,
            }
        )
    df = pd.DataFrame(data)
    if not df.empty:
        df["amr_id"] = df["amr_id"].map(amr_id_mapping)
    st.dataframe(df)


def spawn_amrs():
    try:
        # Create the first instance with amr_id set to AMR.RICK.value
        instance1 = AMRState(amr_id=AMR.RICK.value)
        instance1.save()

        # Create the second instance with amr_id set to AMR.MORTY.value
        instance2 = AMRState(amr_id=AMR.MORTY.value)
        instance2.save()

        st.success("AMRs spawned successfully")

    except Exception as e:
        st.error(f"Error occurred: {e}")


def display_workcell_states():
    # Query all WorkCellState objects
    workcell_states = WorkCellState.objects.all()

    # Prepare data for display
    data = []
    for state in workcell_states:
        workcell_id = state.workcell_id
        active_task = state.active_task if state.active_task else "None"
        docked_amr_id = state.docked_amr_id if state.docked_amr_id else "None"
        data.append(
            {
                "workcell_id": workcell_id,
                "active_task": active_task,
                "docked_amr_id": docked_amr_id,
            }
        )
    df = pd.DataFrame(data)
    if not df.empty:
        df["workcell_id"] = df["workcell_id"].map(workcell_mapping)
        df["docked_amr_id"] = df["docked_amr_id"].map(amr_id_mapping)
    st.dataframe(df)


def spawn_workcells():
    try:
        for workcell_id in WorkCell:
            if workcell_id == WorkCell.UNDEFINED:
                continue
            instance = WorkCellState(workcell_id=workcell_id.value)
            instance.save()

        st.success("WorkCells spawned successfully")

    except Exception as e:
        st.error(f"Error occurred: {e}")


######### GUI Layout #########

st.title("Testbed Control Panel")

# GUI Elements
st.markdown("## All Assembly Workflows")

# Fetch and display AssemblyWorkflows
workflow_data = fetch_assembly_workflows()
st.dataframe(workflow_data)

# Button to delete all instances
if st.button("Delete All Assembly Workflows, Task Chains and Tasks", use_container_width=True):
    delete_all_assembly_workflows()

st.markdown("## Testbed Assets")

st.markdown("### All AMRs")

# Call the function in your Streamlit app
display_amr_states()

if st.button("Spawn AMRs", use_container_width=True):
    spawn_amrs()

st.markdown("### All WorkCells")

display_workcell_states()

if st.button("Spawn WorkCells", use_container_width=True):
    spawn_workcells()


# def get_workflow_status(workflow_id):
#     workflow = AssemblyWorkflow.objects.get(id=workflow_id)
#     details = {
#         "ID": workflow.id,
#         "Model Assembly Type ID": workflow.model_assembly_type_id,
#         # Add more fields from AssemblyWorkflow if necessary
#     }

#     # Existing logic to fetch details from 'Fetch Parts Bins Task' and 'Transport Parts Bins to Kitting Station Task Chain'
#     # ...

#     # Transport Kitting Task Payload to Assembly Station Task Chain
#     transport_kitting_to_assembly = workflow.transport_kitting_task_payload_to_assembly_station
#     if transport_kitting_to_assembly:
#         details['Transport Kitting to Assembly Station'] = {
#             "Navigate to Source": str(transport_kitting_to_assembly.navigate_to_source_subtask) if transport_kitting_to_assembly.navigate_to_source_subtask else "None",
#             "Loading Subtask": str(transport_kitting_to_assembly.loading_subtask) if transport_kitting_to_assembly.loading_subtask else "None",
#             "Navigate to Sink": str(transport_kitting_to_assembly.navigate_to_sink_subtask) if transport_kitting_to_assembly.navigate_to_sink_subtask else "None",
#             "Unloading Subtask": str(transport_kitting_to_assembly.unloading_subtask) if transport_kitting_to_assembly.unloading_subtask else "None",
#         }
#     else:
#         details['Transport Kitting to Assembly Station'] = "None"

#     # Kitting Task
#     details['Kitting Task'] = str(workflow.kitting_task) if workflow.kitting_task else "None"

#     # Transport Assembly Task Payload to QA Station Task Chain
#     transport_assembly_to_qa = workflow.transport_assembly_task_payload_to_qa_station
#     if transport_assembly_to_qa:
#         details['Transport Assembly to QA Station'] = {
#             "Navigate to Source": str(transport_assembly_to_qa.navigate_to_source_subtask) if transport_assembly_to_qa.navigate_to_source_subtask else "None",
#             "Loading Subtask": str(transport_assembly_to_qa.loading_subtask) if transport_assembly_to_qa.loading_subtask else "None",
#             "Navigate to Sink": str(transport_assembly_to_qa.navigate_to_sink_subtask) if transport_assembly_to_qa.navigate_to_sink_subtask else "None",
#             "Unloading Subtask": str(transport_assembly_to_qa.unloading_subtask) if transport_assembly_to_qa.unloading_subtask else "None",
#         }
#     else:
#         details['Transport Assembly to QA Station'] = "None"

#     # Assembly Task
#     details['Assembly Task'] = str(workflow.assembly_task) if workflow.assembly_task else "None"

#     return details
