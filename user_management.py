import streamlit as st
import json
import os
from file_input import load_person_data

# Save data back to the JSON file
def save_data(data):
    with open("data/person_db.json", 'w') as file:
        json.dump(data, file, indent=4)

# Function to get the next free ID
def get_next_id(data):
    if data:
        return max(user['id'] for user in data) + 1
    else:
        return 1

# Function to get the next free EKG ID
def get_next_ekg_id(data):
    ekg_ids = [ekg['id'] for user in data for ekg in user['ekg_tests']]
    if ekg_ids:
        return max(ekg_ids) + 1
    else:
        return 1

# Function to validate new user data
def validate_user(user):
    if not user['firstname'] or not user['lastname'] or not user['date_of_birth']:
        return False, "Please fill in all required fields."
    for ekg in user['ekg_tests']:
        if not ekg['id'] or not ekg['date'] or not ekg['result_link']:
            return False, "Please fill in all EKG test details."
    return True, ""

# Function to save uploaded file with conflict resolution
def save_uploaded_file(uploaded_file, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    file_root, file_ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{file_root}_{counter}{file_ext}"
        counter += 1
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to delete uploaded files
def delete_uploaded_files(files):
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'basic_info' not in st.session_state:
    st.session_state.basic_info = {}
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'file_info' not in st.session_state:
    st.session_state.file_info = []

# Load existing data
data = load_person_data()

# Functions to reset the state
def reset_state():
    st.session_state.step = 0
    st.session_state.basic_info = {}
    st.session_state.uploaded_files = []
    st.session_state.file_info = []

def new_user():
    st.write(f"Entering new_user function, current step: {st.session_state.step}")

    # Step 1: Add basic information
    if st.session_state.step == 1:
        st.write("Step 1: Add basic information")
        st.header('Step 1: Basic Information')
        with st.form(key='basic_info_form'):
            firstname = st.text_input('First Name')
            lastname = st.text_input('Last Name')
            date_of_birth = st.number_input('Date of Birth', min_value=1900, max_value=2024, step=1)
            submit_button = st.form_submit_button(label='Next')

            if submit_button:
                st.session_state.basic_info = {
                    'id': get_next_id(data),
                    'firstname': firstname,
                    'lastname': lastname,
                    'date_of_birth': date_of_birth,
                    'sex': '',
                    'picture_path': '',
                    'ekg_tests': []
                }
                st.session_state.step = 2
                st.experimental_rerun()

    # Step 2: Upload files
    if st.session_state.step == 2:
        st.write("Step 2: Upload files")
        st.header('Step 2: Upload Files')
        picture = st.file_uploader('Upload Picture', type=['jpg', 'png', 'jpeg'])
        ekg_files = st.file_uploader('Upload EKG Test Results', type=['txt', 'pdf', 'fit'], accept_multiple_files=True)
        if st.button('Next', key='step2_next'):
            if picture:
                picture_path = save_uploaded_file(picture, 'data/pictures')
                st.session_state.basic_info['picture_path'] = picture_path
                st.session_state.uploaded_files.append(picture_path)
            for ekg_file in ekg_files:
                if ekg_file.name.endswith('.fit'):
                    result_link = save_uploaded_file(ekg_file, 'data/fit_files')
                else:
                    result_link = save_uploaded_file(ekg_file, 'data/ekg_data')
                st.session_state.uploaded_files.append(result_link)
                st.session_state.basic_info['ekg_tests'].append({
                    'id': get_next_ekg_id(data),
                    'date': '',
                    'result_link': result_link
                })
            st.session_state.step = 3
            st.experimental_rerun()

    # Step 3: Enter file information
    if st.session_state.step == 3:
        st.write("Step 3: Enter file information")
        st.header('Step 3: Enter File Information')
        for i, ekg_test in enumerate(st.session_state.basic_info['ekg_tests']):
            ekg_test['date'] = st.text_input(f'EKG Test Date for {os.path.basename(ekg_test["result_link"])}', key=f'ekg_date_{i}')
        if st.button('Next', key='step3_next'):
            st.session_state.step = 4
            st.experimental_rerun()

    # Step 4: Confirm information and save
    if st.session_state.step == 4:
        st.write("Step 4: Confirm information and save")
        st.header('Step 4: Confirm Information')
        st.json(st.session_state.basic_info)
        if st.button('All info correct/continue', key='step4_confirm'):
            new_user = st.session_state.basic_info
            is_valid, validation_message = validate_user(new_user)
            if is_valid:
                data.append(new_user)
                save_data(data)
                st.success('User added successfully!')
                if st.button('Add New User', key='add_new_user'):
                    reset_state()
                    st.experimental_rerun()
                if st.button('Leave', key='leave'):
                    st.stop()
            else:
                st.error(validation_message)
                delete_uploaded_files(st.session_state.uploaded_files)
                st.session_state.step = 2
                st.experimental_rerun()
        if st.button('Revoke/Start Again', key='step4_revoke'):
            reset_state()
            st.experimental_rerun()
    return True