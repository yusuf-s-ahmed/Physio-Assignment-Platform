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

# Title
st.title("Patient Database Search Tool")

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

# Function to fetch patients whose names start with a specific letter
def fetch_patients_by_letter(letter):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Use the correct column names from the patients table
    query = "SELECT id, name FROM patients WHERE name LIKE %s"
    cursor.execute(query, (letter + '%',))  # Fetch patients where the name starts with the letter
    results = cursor.fetchall()
    connection.close()
    return results

# Function to fetch the first 100 patients alphabetically
def fetch_first_100_patients():
    connection = connect_to_database()
    cursor = connection.cursor()

    # Use the correct column names from the patients table
    query = "SELECT id, name FROM patients ORDER BY name ASC LIMIT 100"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

# User input to search by the first letter of the patient's name
letter = st.text_input("Enter the first letter of the patient's name to search:")

if letter:
    patients = fetch_patients_by_letter(letter)
    if patients:
        st.subheader(f"Patients with names starting with '{letter}':")
        for patient in patients:
            st.write(f"Patient ID: {patient[0]}, Patient Name: {patient[1]}")
    else:
        st.write("No patients found with that letter.")

st.markdown("<p>", unsafe_allow_html=True)  # Adds vertical spacing

# Button to load the patient database
if st.button("Load Patient Database"):
    st.subheader("First 100 Patients (Alphabetical Order):")
    patients = fetch_first_100_patients()
    for patient in patients:
        st.write(f"Patient ID: {patient[0]}, Patient Name: {patient[1]}")
