import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from PIL import Image
import streamlit as st
import os
import time
import json
from file_input import load_person_data, get_person_list, get_image_path, get_ecg_path, read_ecg_data


# Make ECG plot with the possibility to mark peaks
def ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks):
    max_seconds = len(df_ecg_data) // 500
    selected_area_start = 500 * st.number_input("Start of the selected area (in s) :", min_value=0,
                                                max_value=max_seconds, value=0)
    selected_area_end = (500 * st.number_input("End of the selected area (in s) :", min_value=0,
                                               max_value=max_seconds, value=max_seconds))

    if selected_area_start < selected_area_end:
        filtered_df_ecg = df_ecg_data.iloc[selected_area_start:selected_area_end]
        filtered_df_ecg["Zeit in s"] = filtered_df_ecg["Zeit in ms"] / 1000  # Scale x-axis to seconds
        fig_ecg_marked = px.line(filtered_df_ecg, x="Zeit in s", y="Messwerte in mV")
        fig_ecg_marked.update_layout(title="ECG Data", xaxis_title="Time in ms", yaxis_title="Voltage in mV")
    else:
        st.error("Start value must be less than end value.")
        fig_ecg_marked = px.line()

    if checkbox_mark_peaks:
        fig_ecg_marked.add_trace(go.Scatter(x=df_ecg_data.iloc[peaks[0]]["Zeit in ms"] / 1000,
                                            y=df_ecg_data.iloc[peaks[0]]["Messwerte in mV"],
                                            mode="markers",
                                            marker=dict(size=5, color="red"),
                                            name="Peak"))
        st.write("MARKED PEAKS")
    else:
        pass

    return fig_ecg_marked
