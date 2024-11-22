import streamlit as st
import mysql.connector

# Set page config at the very start
st.set_page_config(
    page_title="Physio Exercise Assignment App",
    page_icon="🏋️‍♂️",
)

# Custom CSS
st.markdown("""
    <style>
    /* Import Roboto font for a more medical, professional look */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Change the background color */
    .stApp {
        background-color: #18191c;
    }

    /* Change the color of the sidebar */
    .css-1d391kg {  /* Inspect to confirm this class */
        background-color: #35383b; /* Darker than the background */
    }

    /* Style for the navbar */
    .stToolbar {
        background-color: #35383b; /* Darker than the main background */
    }

    /* Change styles for selectable boxes */
    .stSelectbox, .stCheckbox, .stRadio {
        background-color: transparent; /* Make the main background transparent */
        border-radius: 5px; /* Optional: rounded corners */
        border: none; /* Remove the default border */
        box-shadow: none; /* Remove shadow if any */
        outline: none; /* Remove the default outline */
    }

    /* Make the inner sections of selectable boxes darker */
    .stSelectbox div:first-child,
    .stCheckbox div:first-child,
    .stRadio div:first-child {
        background-color: transparent; /* Make the top section transparent */
        color: #ababab; /* Text color inside the selectable boxes */
    }

    /* Ensure bottom part of selectable boxes has a darker background */
    .stSelectbox div:not(:first-child),
    .stCheckbox div:not(:first-child),
    .stRadio div:not(:first-child) {
        background-color: #35383b; /* Dark background for options */
        color: #ababab; /* Text color for options */
    }

    /* Set focus styles to none to prevent outline */
    .stSelectbox:focus, .stCheckbox:focus, .stRadio:focus {
        outline: none; /* Remove outline on focus */
        box-shadow: none; /* Remove any focus shadow */
    }

    /* Change font style and size for the title */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 36px;
        color: #ababab;
        font-weight: 300; /* Medium weight for the title */
    }

    
    h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 370; /* Lighter weight for regular text */
        color: #ababab; /* Light grey text color */
        font-size: 20px;
        
    }

    /* Set regular text (paragraphs) to lighter font weight */
    p, div, span, label {
        font-family: 'Roboto', sans-serif;
        font-weight: 300; /* Lighter weight for regular text */
        color: #ababab; /* Light grey text color */
    }

    /* Style for buttons */
    .stButton button {
        background-color: #455a63;
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        padding: 6px;
        border-radius: 5px;
        border: none; /* Ensure no border on buttons */   
        color: white;
    }

    .stButton button:hover {
        background-color: #688896;
        color: white;
    }

    /* Style for sliders */
    .stSlider .st-1l9uh0ax {
        color: #ff5733;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Patient Management")

# Database connection parameters
db_user = "------------"
db_password = "-----------"
db_host = "q---.eu-west-1.rds.amazonaws.com"
db_port = ----
db_database = "d---"

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

# Function to add a new patient
def add_patient(name, email, phone, previous_exercise, history):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("INSERT INTO patients (name, email, phone_number, previous_exercise, history) "
             "VALUES (%s, %s, %s, %s, %s)")
    values = (name, email, phone, previous_exercise, history)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Function to update patient details
def update_patient(id, name, email, phone, previous_exercise, history):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("UPDATE patients SET name = %s, email = %s, phone_number = %s, previous_exercise = %s, history = %s "
             "WHERE id = %s")
    values = (name, email, phone, previous_exercise, history, id)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Function to delete a patient
def delete_patient(id):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "DELETE FROM patients WHERE id = %s"
    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()

# Function to view patient details
def view_patient(id):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM patients WHERE id = %s"
    cursor.execute(query, (id,))
    patient = cursor.fetchone()

    cursor.close()
    conn.close()
    return patient



# View patient details
st.subheader("View Patient Details")
view_patient_id = st.number_input("Enter Patient ID to View", min_value=1, step=1)

if st.button("View Patient"):
    if view_patient_id:
        patient = view_patient(view_patient_id)
        if patient:
            st.write(f"Patient ID: {patient[0]}")
            st.write(f"Name: {patient[1]}")
            st.write(f"Email: {patient[2]}")
            st.write(f"Phone Number: {patient[3]}")
            st.write(f"Previous Exercise: {patient[4]}")
            st.write(f"History: {patient[5]}")
        else:
            st.error("No patient found with this ID.")
    else:
        st.error("Please provide a patient ID to view.")

# Add new patient
st.subheader("Add New Patient")
patient_name = st.text_input("Patient Name")
patient_email = st.text_input("Patient Email")
patient_phone = st.text_input("Patient Phone Number")
previous_exercise = st.text_input("Previous Exercise")
history = st.text_area("History")

if st.button("Add Patient"):
    if patient_name and patient_email and patient_phone and previous_exercise and history:
        add_patient(patient_name, patient_email, patient_phone, previous_exercise, history)
        st.success("Patient added successfully!")
    else:
        st.error("Please provide all required information.")

# Update patient
st.subheader("Update Patient")
patient_id = st.number_input("Patient ID to Update", min_value=1, step=1)
updated_patient_name = st.text_input("Updated Patient Name")
updated_patient_email = st.text_input("Updated Patient Email")
updated_patient_phone = st.text_input("Updated Patient Phone Number")
updated_previous_exercise = st.text_input("Updated Previous Exercise")
updated_history = st.text_area("Updated History")

if st.button("Update Patient"):
    if patient_id and updated_patient_name and updated_patient_email and updated_patient_phone and updated_previous_exercise and updated_history:
        update_patient(patient_id, updated_patient_name, updated_patient_email, updated_patient_phone, updated_previous_exercise, updated_history)
        st.success("Patient updated successfully!")
    else:
        st.error("Please provide all required information.")

# Delete patient
st.subheader("Delete Patient")
delete_patient_id = st.number_input("Patient ID to Remove", min_value=1, step=1)

if st.button("Remove Patient"):
    if delete_patient_id:
        delete_patient(delete_patient_id)
        st.success("Patient removed successfully!")
    else:
        st.error("Please provide a patient ID to remove.")

