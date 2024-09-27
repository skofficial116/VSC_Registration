import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("vsv-form-8b53e090ee84.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("Vedic_Science_Club_Form").worksheet("Registration")

# Load existing data from Google Sheet into a DataFrame
existing_data = pd.DataFrame(sheet.get_all_records())

# Logo URL
logo_path = "https://www.socet.edu.in/clubs/images/clubs/Vedic.png"

# Desktop and Mobile background image URLs
desktop_bg_image_url = "https://i.pinimg.com/564x/07/98/a6/0798a638b3ea2202395f29a82497c89a.jpg"
mobile_bg_image_url = "https://i.pinimg.com/564x/61/aa/c0/61aac0be49bb35d105a3f28465403597.jpg"

# Configure Streamlit page
st.set_page_config(page_title="VSC Registrations", layout='wide')

# CSS for media queries and styling form input fields
media_query_css = f"""
    <style>
    /* Desktop view */
    @media (min-width: 768px) {{
        [data-testid="stAppViewContainer"] {{
            background-image: url("{desktop_bg_image_url}");
            background-size: cover;
            background-position: center;
        }}
    }}

    /* Mobile view */
    @media (max-width: 767px) {{
        [data-testid="stAppViewContainer"] {{
            background-image: url("{mobile_bg_image_url}");
            background-size: cover;
            background-position: center;
        }}
    }}
    
    .stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}
    
    .stSelectbox div {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}
    
    .stTextArea textarea {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}
    
    #kindly-fill-your-information{{color: black;}}    
    
    /* Style the labels of select boxes and text inputs */
    label {{font-size: 30px;
        color: #ffffff !important;
    }}

    /* Dark theme form container */
    .form-container {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 10px;
        color: #ffffff;
    }}

    /* Center the logo */
    .center-img {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}
    
    .stSelectbox div {{
    background-color: white !important;
    color: black !important;
}}

    /* Center the dialog content */
    .center-dialog {{
        text-align: center;
    }}

    /* Background color for "Kindly Fill Your Information" */
    .info-header {{
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        color: black;
    }}
    </style>
"""
st.markdown(media_query_css, unsafe_allow_html=True)

# Display the logo in the center
st.markdown(f"<div class='center-img'><img src='{logo_path}' width='300'></div>", unsafe_allow_html=True)

# "Kindly fill your information" with a white background
st.markdown("<div class='info-header'><h2 style='text-align: center;'>Kindly fill your information</h2></div>", unsafe_allow_html=True)

# Form styling
form_style = """
<div class='form-container'>
    <h3 style='color: #ffffff;'>Registration Form</h3>
"""

# Create the registration form
with st.form(key="Registration"):
    st.markdown(form_style, unsafe_allow_html=True)
    name = st.text_input("Name *")
    course, section, year = st.columns(3, vertical_alignment="bottom")
    st.divider()
    
    with course:
        course = st.text_input("Course *")
        
    with section:
        section = st.text_input("Section *")
        
    with year:
        year = st.selectbox("Current Year *", ["First", "Second", "Third", "Fourth"])
    
    email = st.text_input("E-Mail *")
    st.divider()
    phone = st.text_input("Phone Number *")
    st.divider()
    gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
    st.divider()
    interest = st.selectbox(
        "Which field are you interested in? *",
        [
            "Content Creation",
            "Social Media",
            "Anchoring",
            "Management",
            "Music",
            "Others",
        ],
    )
    st.divider()
    
    submit_button = st.form_submit_button(label="Submit")

# Modal dialog function to show a welcome message including the user's name
@st.dialog("Vedic Science Club team")
def thanks(name):
    st.markdown(f"<div class='center-img'><img src='{logo_path}' width='300'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='center-dialog'>
            <h1 style='color: #0b9ff9; font-size: 35px'>Vedic Science Club</h1>
            <p style='color: #0b9ff9; font-size: 19px'>
                Hare Krishna, {name}! Welcome to the Vedic Science Club! We are excited to have you on board as we embark on this enlightening journey of exploring ancient wisdom through modern perspectives. Stay tuned for updates and engaging sessions that will deepen your understanding of Vedic knowledge!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Check for duplicate entries and form validation
if submit_button:
    if not name or not course or not section or not email or not phone or not gender or not interest:
        st.warning("All fields are required. Please fill out every field.")
    else: 
        new_data = pd.DataFrame([{
            "name": name,
            "gender": gender,
            "section": section,
            "year": year,
            "course": course,
            "email": email,
            "phone": phone,
            "interest": interest,
        }])
        
        # Convert DataFrame to list of lists and append to the Google Sheet
        sheet.append_row(new_data.iloc[0].tolist())
        
        st.markdown(
            f"<h4 style='background-color: green; color: white; text-align: center;display: block; padding: 5px 20px;'>Thank you, {name}! Your registration has been successfully recorded.</h4>",
            unsafe_allow_html=True
        )
        
        # Call the thanks function to display the dialog with the name
        thanks(name)
