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
import json
from file_input import load_person_data, get_person_list, get_image_path, get_ecg_path, read_ecg_data


def ecg_plot(df_ecg_data):
    fig = px.line(df_ecg_data.head(2000), x="Zeit in ms", y="Messwerte in mV")
    fig.update_layout(title="ECG Data", xaxis_title="Time in ms", yaxis_title="Voltage in mV")


    return fig