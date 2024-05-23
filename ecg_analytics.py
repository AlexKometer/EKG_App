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

from file_input import read_ecg_data

"""
sampling_frequency = 500 # Hz
"""


# Function to detect peaks in the ECG data, Output is an array of heart rates
def peak_detection(path):
    df = read_ecg_data(path)
    peaks = sc.signal.find_peaks(df["Messwerte in mV"], height=350)

    return peaks


# Function to calculate heart rate statistics
def calculate_hr_data(peaks):
    peak_interval = np.diff(peaks[0])
    peak_interval_seconds = peak_interval / 1000
    hr = np.round(60 / peak_interval_seconds, 0)
    hr_max = hr.max()
    hr_min = hr.min()
    hr_mean = hr.mean()

    return hr, hr_max, hr_min, hr_mean

print(peak_detection("data/ekg_data/01_Ruhe.txt"))