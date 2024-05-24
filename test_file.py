import streamlit as st
import json
import os
import webbrowser

# Load existing data from the JSON file
def load_person_data():
    with open("data/person_db.json", 'r') as file:
        person_data = json.load(file)
    return person_data

# Save data back to the JSON file
def save_data(data):
    with open("data/person_db.json", 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a new user
def add_user(data, new_user):
    data.append(new_user)
    save_data(data)

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
    if not user['firstname'] or not user['lastname'] or not user['sex'] or not user['date_of_birth']:
        return False, "Please fill in all required fields."
    for ekg in user['ekg_tests']:
        if not ekg['id'] or not ekg['date'] or not ekg['result_link']:
            return False, "Please fill in all EKG test details."
    return True, ""

# Function to save uploaded file
def save_uploaded_file(uploaded_file, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Streamlit app
st.title('User Management')

# Button to open a new tab to add a new user
if st.button('Add New User'):
    webbrowser.open_new_tab('http://localhost:8501/?add_user=true')

# Load existing data
data = load_person_data()

# Add User Page
query_params = st.experimental_get_query_params()
if 'add_user' in query_params:
    st.title('Add New User')

    # User input form
    with st.form(key='add_user_form'):
        id = get_next_id(data)
        st.write(f'ID: {id}')
        date_of_birth = st.number_input('Date of Birth', min_value=1900, max_value=2024, step=1)
        firstname = st.text_input('First Name')
        lastname = st.text_input('Last Name')
        picture = st.file_uploader('Upload Picture', type=['jpg', 'png', 'jpeg'])
        sex = st.selectbox('Sex', ['male', 'female'])

        ekg_tests = []
        ekg_files = st.file_uploader('Upload EKG Test Results', type=['txt', 'pdf', 'fit'], accept_multiple_files=True)
        for ekg_file in ekg_files:
            ekg_id = get_next_ekg_id(data)
            date = st.text_input(f'EKG Test Date for {ekg_file.name}', key=f'ekg_date_{ekg_id}')
            if ekg_file.name.endswith('.fit'):
                result_link = save_uploaded_file(ekg_file, 'data/fit_files')
            else:
                result_link = save_uploaded_file(ekg_file, 'data/ekg_data')
            ekg_tests.append({
                'id': ekg_id,
                'date': date,
                'result_link': result_link
            })

        # Submit button
        submit_button = st.form_submit_button(label='Add User')

        if submit_button:
            picture_path = ''
            if picture:
                picture_path = save_uploaded_file(picture, 'data/pictures')

            new_user = {
                'id': id,
                'date_of_birth': date_of_birth,
                'firstname': firstname,
                'lastname': lastname,
                'picture_path': picture_path,
                'sex': sex,
                'ekg_tests': ekg_tests
            }
            is_valid, validation_message = validate_user(new_user)
            if is_valid:
                add_user(data, new_user)
                st.success('User added successfully!')
            else:
                st.error(validation_message)
else:
    st.subheader('User List')
    if st.button('Show Users'):
        st.json(data)
