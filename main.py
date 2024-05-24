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
import time
import json

from file_input import load_person_data, get_person_list, get_image_path, get_ecg_path, read_ecg_data, calculate_person_age, get_year_of_birth, get_ekg_test_date, get_sex
from create_plot import ecg_plot
from ecg_analytics import peak_detection, calculate_hr_data, estimated_max_hr
from user_management import new_user, reset_state

# Load basic data
person_dict = load_person_data()
person_names = get_person_list(person_dict)

sf = 500

# Streamlit settings
st.set_page_config(layout="wide")
st.title("ECG-APP")

# Sidebar
st.sidebar.header("Navigation")
current_user = st.sidebar.radio('Subject:', options=person_names, key="sbVersuchsperson")

button_new_user = st.sidebar.button("New User", key="btnNewUser")
button_edit_user = st.sidebar.button("Edit User", key="btnEditUser")
button_delete_user = st.sidebar.button("Delete User 🗑️", key="btnDeleteUser")
st.sidebar.write("")
checkbox_mark_peaks = st.sidebar.checkbox("Mark Peaks", value=False, key="cbMarkPeaks")

if button_new_user:
    st.session_state.step = 1
    st.session_state.basic_info = {}
    new_user()
elif st.session_state.get("step", 0) > 0:
    new_user()
elif button_edit_user:
    st.write("Edit user functionality is not implemented yet.")
elif button_delete_user:
    st.write("Delete user functionality is not implemented yet.")
else:
    tab1, tab2, tab3 = st.tabs([current_user, "ECG", "HR Analysis"])
    with tab1:
        st.write("#### General Information:", current_user)
        image = Image.open(get_image_path(person_dict, current_user))
        st.image(image, caption=current_user)
        st.write("The Year of Birth is: ", get_year_of_birth(person_dict, current_user))
        st.write("The age of the subject is: ", calculate_person_age(person_dict, current_user))
        ecg_path = get_ecg_path(person_dict, current_user)
        test_date = get_ekg_test_date(person_dict, current_user)
        st.write("")
        st.write("### Number of ECGs: ", len(ecg_path))

        for i in range(len(ecg_path)):
            st.write("")
            st.write("Test date: ", test_date[i], ":")
            st.write("ECG " + str(i + 1) + ": ", ecg_path[i])
            st.write("Length of the test in seconds: ",
                     int(np.round(len(read_ecg_data(ecg_path[i])) / 500, 0)))

    with tab2:
        selected_ecg_path = st.selectbox('ECG:', options=ecg_path, key="sbECG")
        df_ecg_data = read_ecg_data(selected_ecg_path)
        peaks = peak_detection(selected_ecg_path)
        st.plotly_chart(ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf))

        st.write("This ecg was recorded on: ", test_date[ecg_path.index(selected_ecg_path)])

    with tab3:
        st.write("This is tab 3")
        hr, hr_max, hr_min, hr_mean = calculate_hr_data(peak_detection(selected_ecg_path))

        st.write("The maximum heart rate is: ", hr_max)
        st.write("The minimum heart rate is: ", hr_min)
        st.write("The mean heart rate is: ", hr_mean)
        st.write("The estimated maximum heart rate is: ",
                 estimated_max_hr(calculate_person_age(person_dict, current_user), get_sex(person_dict, current_user)))


# TODO MUST DO
#  Geburtsjahr, Name und Bild der Personen wird angezeigt (2pkt) --> Done
#  Auswahlmöglichkeit für Tests, sofern mehr als ein Test bei einer Person vorliegt (4pkt) --> Done
#  Anzeigen des Testdatums und der gesamtem Länge der Zeitreihe in Sekunden (4pkt) --> Done
#  EKG-Daten werden beim Einlesen sinnvoll resampelt, um Ladezeiten zu verkürzen (2pkt) --> Done
#  Sinnvolle Berechnung der Herzrate über den gesamten Zeitraum wird angezeigt (2pkt) --> Done
#  Nutzer:in kann sinnvollen Zeitbereich für Plots auswählen (2pkt) --> Done
#  Stil z.B. Namenskonventionen, sinnvolle Aufteilung in Module, Objektorientierung (4pkt)
#  Kommentare und Docstrings (2pkt)
#  Design für Computer Bildschirm optimiert und optisch ansprechend (2pkt)
#  Deployment auf Heroku oder Streamlit Sharing (2pkt)


# TODO: optional
#  Daten aus einer anderen Datenquelle einlesen (z.B. .fit oder kml) (4pkt)
#  Neue Daten mit einem Nutzer verknüpfen (4pkt)
#  Nutzer und Test-Daten editierbar machen (4pkt)
#  Daten in einer SQLite oder tinyDB speichern (6pkt)
#  Gefundene Peaks im Plot anzeigen (2pkt) --> Done
#  Herzrate im sinnvollen gleitenden Durchschnitt als Plot anzeigen (2pkt)
#  Ausrechnen des Maximalpuls basierend auf Alter. Anzeige im Dashboard (1pkt) --> Done
#  Herzratenvariabilität anzeigen (2pkt)
#  Weitere eigene: Vorzustellen in Pitch-Sessiona
