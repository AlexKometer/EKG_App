import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
from PIL import Image
import os
import json

from file_input import load_person_data, get_person_list, get_image_path, get_ecg_path, read_ecg_data, calculate_person_age
from create_plot import ecg_plot

st.title("ECG-APP")
st.write("## Choose subject:")

person_dict = load_person_data()
person_names = get_person_list(person_dict)

current_user = st.selectbox('Subject:', options=person_names, key="sbVersuchsperson")
image = Image.open(get_image_path(person_dict, current_user))
st.image(image, caption=current_user)

#st.write("The name of the subject is: " + current_user)
#st.write("The image path is: " + get_image_path(person_dict, current_user))

ecg_path = get_ecg_path(person_dict, current_user)

#st.write("The ECG paths: " + ", ".join(ekg_paths))

tab1, tab2, tab3 = st.tabs(["Subject Information", "ECG", "Tab 3"])
with tab1:
    st.write("This is tab 1")
    st.write("The name of the subject is: " + current_user)
    st.write("The age of the subject is: " + calculate_person_age(person_dict, current_user))

with tab2:
    st.write("This is tab 1")
    selected_ecg_path = st.selectbox('ECG:', options=ecg_path, key="sbECG")
    df_ecg_data = read_ecg_data(selected_ecg_path)
    st.plotly_chart(ecg_plot(df_ecg_data))

with tab3:
    st.write("This is tab 3")