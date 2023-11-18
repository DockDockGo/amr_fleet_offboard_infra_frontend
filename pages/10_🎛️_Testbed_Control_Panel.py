import streamlit as st
import os
import django
from pathlib import Path
import sys
import pandas as pd

# Path to the directory of your Django project
django_project_path = "/Users/sid/courses/Project/offboard_infra/testbed_emulator_backend/testbed_emulator_backend"
sys.path.insert(0, django_project_path)

# Django project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testbed_emulator_backend.settings")

# Set up Django
django.setup()

from testbed_emulator_backend_app.models import *  # Replace 'yourapp' with the name of your Django app

from testbed_emulator_backend_app.models import (
    AssemblyWorkflow,
    TestbedTask,
    MaterialTransportTaskChain,
)

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

st.title("Testbed Control Panel")

# GUI Elements
st.markdown("## Assembly Workflows")

# Fetch and display AssemblyWorkflows
workflow_data = fetch_assembly_workflows()
st.dataframe(workflow_data)

# Button to delete all instances
if st.button('Delete All Data'):
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

        st.success('All data has been deleted from the database')

    except Exception as e:
        st.error(f'Error occurred: {e}')

st.write(
    "Display the current finite state machine states of all active assemblies in the testbed here, along with buttons to send commands to interface with the AMR fleet API."
)


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



