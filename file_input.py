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

    for entry in person_data:
        list_of_names.append(entry["lastname"] + ", " + entry["firstname"])
    return list_of_names


def get_image_path(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            return entry["picture_path"]
    return None

def get_sex(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            return entry["sex"]
    return None

def get_year_of_birth(person_dict, current_user):
    for person in person_dict:
        full_name = f"{person['lastname']}, {person['firstname']}"
        if full_name == current_user:
            return person["date_of_birth"]
    return None


def calculate_person_age(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            age = datetime.now().year - entry["date_of_birth"]
            return age
    return []

def get_ecg_path(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            return [test["result_link"] for test in entry["ekg_tests"]]
    return []


def get_ekg_test_date(person_data, person_name):
    for entry in person_data:
        if person_name == entry["lastname"] + ", " + entry["firstname"]:
            return [test["date"] for test in entry["ekg_tests"]]
    return []


def read_ecg_data(ecg_path):
    df_ecg_data = pd.read_csv(ecg_path, sep="\t", header=None)
    df_ecg_data.columns = ["Messwerte in mV", "Zeit in ms"]
    df_ecg_data["Zeit in ms"] = df_ecg_data["Zeit in ms"] - df_ecg_data["Zeit in ms"].iloc[0]

    return df_ecg_data


def read_power_data(power_path):
    df_power_data = pd.read_csv(power_path, sep="\t", header=None)

    return df_power_data
