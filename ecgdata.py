import json
import pandas as pd
import plotly.express as px
import streamlit as st
import scipy as sc
import numpy


# %% Objekt-Welt

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])

    def load_by_id(suchstring):
        file = open("data/person_db.json")
        person_data = json.load(file)

        if suchstring == "None":
            return {}

        for eintrag in person_data:
            search =  eintrag['ekg_tests']
            for elements in search:
                if (elements['id'] == suchstring):
                    return elements

        else:
            return {}

    def read_ecg_data(ecg_path):
        df_ecg_data = pd.read_csv(ecg_path, sep="\t", header=None)
        df_ecg_data.columns = ["Messwerte in mV", "Zeit in ms"]
        df_ecg_data["Zeit in ms"] = df_ecg_data["Zeit in ms"] - df_ecg_data["Zeit in ms"].iloc[0]

        return df_ecg_data

    def find_peaks(path):

        df = read_ecg_data(path)
        peaks = sc.signal.find_peaks(df["Messwerte in mV"], height=350)
        return peaks


    def estimate_hr(peaks):
        peak_interval = np.diff(peaks[0])
        peak_interval_seconds = peak_interval / 1000
        hr = np.round(60 / peak_interval_seconds, 0)
        hr_mean = np.round(hr.mean(), 0)
        return hr_mean

    def plot_time_series(path):



if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    id = input("ID des EKG: ")
    ekg = EKGdata.load_by_id(id)
    peaks  = find_peaks(ekg['result_link'])
    hr_mean = estimate_hr(peaks)

    plot_time_series(ekg['result_link'])
