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
from datetime import datetime
import json


def load_person_data():
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data


def get_person_list(person_data):
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " + eintrag["firstname"])
    return list_of_names


def get_image_path(person_data, person_name):
    for enty in person_data:
        if person_name == enty["lastname"] + ", " + enty["firstname"]:
            return enty["picture_path"]
    return None

def calculate_person_age(person_data, person_name):
    for entry in person_data:
            if person_name == entry["lastname"] + ", " + entry["firstname"]:
                age = datetime.now().year - entry["date_of_birth"]
            return str(age)


def get_ecg_path(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            return [test["result_link"] for test in entry["ekg_tests"]]
    return []

def read_ecg_data(ecg_path):
    df_ecg_data = pd.read_csv(ecg_path, sep="\t", header=None)
    df_ecg_data.columns = ["Messwerte in mV", "Zeit in ms"]
    return df_ecg_data


def read_power_data(power_path):
    df_power_data = pd.read_csv(power_path, sep="\t", header=None)

    return df_power_data
