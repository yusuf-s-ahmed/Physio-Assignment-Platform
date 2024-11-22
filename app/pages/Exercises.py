import streamlit as st
import mysql.connector

st.set_page_config(
    page_title="Exercise Management",
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

st.title("Exercise Management")


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

# Function to add a new exercise
def add_exercise(name, difficulty, youtube_link, muscle_group):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("INSERT INTO exercises (exercise_name, difficulty, youtube_link, targeted_muscle_group) "
             "VALUES (%s, %s, %s, %s)")
    values = (name, difficulty, youtube_link, muscle_group)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Function to update an exercise
def update_exercise(id, name, difficulty, youtube_link, muscle_group):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("UPDATE exercises SET exercise_name = %s, difficulty = %s, youtube_link = %s, targeted_muscle_group = %s "
             "WHERE id = %s")
    values = (name, difficulty, youtube_link, muscle_group, id)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Function to delete an exercise
def delete_exercise(id):
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "DELETE FROM exercises WHERE id = %s"
    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()

# Function to view all exercises
def view_exercises():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM exercises"
    cursor.execute(query)
    exercises = cursor.fetchall()

    cursor.close()
    conn.close()
    return exercises



# View all exercises
st.subheader("View Exercises")
if st.button("Show All Exercises"):
    exercises = view_exercises()
    if exercises:
        for exercise in exercises:
            st.write(f"ID: {exercise[0]}")
            st.write(f"Name: {exercise[1]}")
            st.write(f"Difficulty: {exercise[2]}")
            st.write(f"YouTube Link: {exercise[3]}")
            st.write(f"Muscle Group: {exercise[4]}")
            st.write("---")
    else:
        st.write("No exercises found.")

# Add new exercise
st.subheader("Add New Exercise")
exercise_name = st.text_input("Exercise Name")
difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
youtube_link = st.text_input("YouTube Link")
muscle_group = st.text_input("Targeted Muscle Group")

if st.button("Add Exercise"):
    if exercise_name and difficulty and youtube_link and muscle_group:
        add_exercise(exercise_name, difficulty, youtube_link, muscle_group)
        st.success("Exercise added successfully!")
    else:
        st.error("Please provide all required information.")

# Update exercise
st.subheader("Update Exercise")
exercise_id = st.number_input("Exercise ID", min_value=1, step=1)
updated_exercise_name = st.text_input("Updated Exercise Name")
updated_difficulty = st.selectbox("Updated Difficulty", ["Beginner", "Intermediate", "Advanced"])
updated_youtube_link = st.text_input("Updated YouTube Link")
updated_muscle_group = st.text_input("Updated Targeted Muscle Group")

if st.button("Update Exercise"):
    if exercise_id and updated_exercise_name and updated_difficulty and updated_youtube_link and updated_muscle_group:
        update_exercise(exercise_id, updated_exercise_name, updated_difficulty, updated_youtube_link, updated_muscle_group)
        st.success("Exercise updated successfully!")
    else:
        st.error("Please provide all required information.")

# Delete exercise
st.subheader("Delete Exercise")
delete_exercise_id = st.number_input("Exercise ID to Remove", min_value=1, step=1)

if st.button("Remove Exercise"):
    if delete_exercise_id:
        delete_exercise(delete_exercise_id)
        st.success("Exercise removed successfully!")
    else:
        st.error("Please provide an exercise ID to remove.")


