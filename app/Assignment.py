import streamlit as st
import mysql.connector
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables
load_dotenv('sendgrid.env')


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
    .css-1d391kg {  
        background-color: #35383b; 
    }

    /* Style for the navbar */
    .stToolbar {
        background-color: #35383b; 
    }

    /* Change styles for selectable boxes */
    .stSelectbox, .stCheckbox, .stRadio {
        background-color: transparent; 
        border-radius: 5px; 
        border: none; 
        box-shadow: none; 
        outline: none; 
    }

    /* Make the inner sections of selectable boxes darker */
    .stSelectbox div:first-child,
    .stCheckbox div:first-child,
    .stRadio div:first-child {
        background-color: transparent; 
        color: #ababab; 
    }

    /* Ensure bottom part of selectable boxes has a darker background */
    .stSelectbox div:not(:first-child),
    .stCheckbox div:not(:first-child),
    .stRadio div:not(:first-child) {
        background-color: #35383b; 
        color: #ababab; 
    }

    /* Set focus styles to none to prevent outline */
    .stSelectbox:focus, .stCheckbox:focus, .stRadio:focus {
        outline: none; 
        box-shadow: none; 
    }

    /* Change font style and size for the title */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 36px;
        color: #ababab;
        font-weight: 300; 
    }

    h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 370; 
        color: #ababab; 
        font-size: 20px;
    }

    /* Set regular text (paragraphs) to lighter font weight */
    p, div, span, label {
        font-family: 'Roboto', sans-serif;
        font-weight: 300; 
        color: #ababab; 
    }

    /* Style for buttons */
    .stButton button {
        background-color: #455a63;
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        padding: 6px;
        border-radius: 5px;
        border: none;  
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

st.title("Patient Exercise Assignment Tool")

# Database connection parameters
db_user = "ty376miw198qbdtc"
db_password = "mpnls4nyljjqrswz"
db_host = "q7cxv1zwcdlw7699.chr7pe7iynqr.eu-west-1.rds.amazonaws.com"
db_port = 3306
db_database = "dn924vi9c6asl4zf"

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

# Function to get patients from the database
def get_patients():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, name FROM patients"
    cursor.execute(query)
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

# Function to get patient history
def get_patient_history(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT history FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    history = cursor.fetchone()
    cursor.close()
    conn.close()
    return history['history'] if history else ""

# Function to get patient email
def get_patient_email(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT email FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    email = cursor.fetchone()
    cursor.close()
    conn.close()
    return email['email'] if email else ""

# Function to get patient documents
def get_patient_documents(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT document_url, document_description FROM patient_documents WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

# Function to get exercises based on difficulty
def get_exercises(difficulty):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT exercise_name, youtube_link FROM exercises WHERE difficulty = %s"
    cursor.execute(query, (difficulty,))
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()
    return exercises

# Function to get YouTube thumbnail URL
def get_thumbnail_url(youtube_link):
    video_id = youtube_link.split('v=')[-1]
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

# Function to automate email sending using SendGrid
def send_email(to_email, subject, body):
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')  # Correctly fetch the API key from the environment
    print(f"Using SendGrid API Key: {sendgrid_api_key}")  # Debug print
    message = Mail(
        from_email='yusufahmed200306@gmail.com',  # Replace with your verified SendGrid email
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        return response.status_code == 202  # SendGrid returns 202 for successful send
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Fetch and display patient data
patients = get_patients()
patient_names = [patient['name'] for patient in patients]
patient_id_map = {patient['name']: patient['id'] for patient in patients}

# Patient selection
patient_name = st.selectbox('Select Patient', patient_names)

if patient_name:
    patient_id = patient_id_map[patient_name]
    history = get_patient_history(patient_id)
    email = get_patient_email(patient_id)
    st.write(f"Patient History for {patient_name}:")
    st.write(history)  # Display the full history string directly

    st.write(f"Patient Email: {email}")  # Display the patient's email

    # Button to view patient data
    if st.button('View Patient Data'):
        st.write(f"Viewing additional data for {patient_name}:")
        
        # Fetch and display patient documents
        documents = get_patient_documents(patient_id)
        if documents:
            st.write("Patient Documents:")
            for doc in documents:
                st.write(f"- [{doc['document_description']}]({doc['document_url']})")  # Display document with description and link
        else:
            st.write("No documents found for this patient.")

# Fetch and display exercises based on difficulty
difficulty = st.selectbox('Select Difficulty Level', ['Beginner', 'Intermediate', 'Advanced'])
exercises = get_exercises(difficulty)
exercise_names = [exercise['exercise_name'] for exercise in exercises]

st.write(f"Select Exercises for {difficulty} level:")
selected_exercises = st.multiselect('Choose exercises', exercise_names)

# Display thumbnails for selected exercises
for exercise_name in selected_exercises:
    for exercise in exercises:
        if exercise['exercise_name'] == exercise_name:
            thumbnail_url = get_thumbnail_url(exercise['youtube_link'])
            st.image(thumbnail_url, caption=exercise_name, use_column_width=True)
            break

# Slider for repetitions
reps = st.slider('Select Repetitions', min_value=1, max_value=15, value=(8, 12), step=1)
st.write(f"Repetitions: {reps[0]} - {reps[1]}")

# Counter for sets
sets = st.number_input('Select Number of Sets', min_value=1, value=1, step=1)

# Additional notes box
additional_notes = st.text_area('Additional Notes', '')

# Button to assign exercises
if st.button('Send Exercises'):
    if patient_name and selected_exercises:
        exercise_list = ", ".join(selected_exercises)
        subject = f"Exercises Assigned to {patient_name}"
        body = f"""
        Dear {patient_name},

        You have been assigned the following exercises:

        Exercises: {exercise_list}
        Repetitions: {reps[0]} - {reps[1]}
        Sets: {sets}
        Additional Notes: {additional_notes}

        Best regards,
        Vital Therapy
        """
        if send_email(email, subject, body):
            st.success("Exercises sent successfully!")
        else:
            st.error("Failed to send exercises.")
    else:
        st.warning("Please select a patient and at least one exercise.")