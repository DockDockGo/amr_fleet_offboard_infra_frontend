import streamlit as st
import time

def amr_departure_countdown(time_s):
    progress_text = "AMR is departing in " + str(time_s) + " seconds. Please stay clear of the AMR!"
    my_bar = st.progress(0, text=progress_text)
    for time_elapsed in range(time_s):
        time.sleep(1)
        time_elapsed += 1
        my_bar.progress(time_elapsed/time_s, text=progress_text)
    my_bar.empty()