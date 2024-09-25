import streamlit as st
import mysql.connector

# Set page config at the very start
st.set_page_config(
    page_title="Patient Document Management",
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

    /* Custom style for warning messages */
    .custom-warning {
        font-family: 'Roboto', sans-serif;
        font-weight: 300;
        color: #fff; /* Highlight color */
        font-size: 15px;
        background-color: #333; /* Light background */
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Patient Document Management")

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

# Function to fetch documents for a specific patient
def fetch_documents(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM patient_documents WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

# Function to fetch patient details
def fetch_patient_details(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()
    return patient

# Function to add a new document
def add_document(patient_id, document_url, document_description):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "INSERT INTO patient_documents (patient_id, document_url, document_description) VALUES (%s, %s, %s)"
    cursor.execute(query, (patient_id, document_url, document_description))
    conn.commit()
    cursor.close()
    conn.close()

# Function to update an existing document
def update_document(doc_id, document_url, document_description):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "UPDATE patient_documents SET document_url = %s, document_description = %s WHERE id = %s"
    cursor.execute(query, (document_url, document_description, doc_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to remove a document
def remove_document(doc_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "DELETE FROM patient_documents WHERE id = %s"
    cursor.execute(query, (doc_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Input for Patient ID
patient_id = st.text_input("Enter Patient ID Number")

if patient_id:
    # Fetch and display patient details
    patient_details = fetch_patient_details(patient_id)
    if patient_details:
        st.write("Patient Details:")
        st.write(f"ID: {patient_details['id']}")
        st.write(f"Name: {patient_details['name']}")
        st.write(f"Email: {patient_details['email']}")
        st.write(f"Phone Number: {patient_details['phone_number']}")
        st.write(f"Previous Exercise: {patient_details['previous_exercise']}")
        st.write(f"History: {patient_details['history']}")

        # View existing documents
        documents = fetch_documents(patient_id)
        if documents:
            st.write("Existing Documents:")
            for doc in documents:
                st.write(f"Name: {doc['document_description']}, URL: {doc['document_url']}")
                
                # Update document option
                if st.button(f"Update Document: {doc['document_description']}"):
                    new_url = st.text_input("New Document URL", value=doc['document_url'], key=f"update_url_{doc['id']}")
                    new_name = st.text_input("New Document Name", value=doc['document_description'], key=f"update_name_{doc['id']}")
                    if st.button("Submit Update", key=f"submit_update_{doc['id']}"):
                        update_document(doc['id'], new_url, new_name)
                        st.success("Document updated successfully!")

                # Remove document option
                if st.button(f"Remove Document: {doc['document_description']}"):
                    remove_document(doc['id'])
                    st.success("Document removed successfully!")
        else:
            st.write("No documents found for this patient.")

        # Add new document section
        st.subheader("Add New Document")
        new_document_url = st.text_input("Document URL")
        new_document_name = st.text_input("Document Name")
        
        if st.button("Add Document"):
            add_document(patient_id, new_document_url, new_document_name)
            st.success("Document added successfully!")
    else:
        st.write("No patient found with this ID.")
else:
    st.markdown('<div class="custom-warning">Please enter a Patient ID to manage documents.</div>', unsafe_allow_html=True)
