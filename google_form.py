import streamlit as st
import pandas as pd

file_path = "C:\\py\\Vedic_Science_Club_Form.xlsx"
logo_path = "C:\\py\\Club_logo.jpg"

page_bg_img = """
    <style>
    [data-testid="stHeader"]
    {
    background-color : rgba(0,0,0,0);
    }
    [data-testid="stAppViewContainer"]
    {
        background-image: url("https://i.pinimg.com/564x/64/29/69/64296974cc1d2bfbd9a97da5190c75df.jpg");
        background-size: auto 100% ;
    }
    </style>
"""
# [data-testid="stAppViewBlockContainer"]
    # {
        
    # }
    # main page block

st.markdown(page_bg_img, unsafe_allow_html=True)



@st.dialog("Vedic Science Club welcomes you!!")
def thanks():
    st.image(logo_path, width=300)
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1 style='color: blue;'>Vedic Science Club</h1>
            <p style='color: green;'>Welcome to the Vedic Science Club! We are excited to have you on board as we embark on this enlightening journey of exploring ancient wisdom through modern perspectives. Stay tuned for updates and engaging sessions that will deepen your understanding of Vedic knowledge!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.logo(logo_path, icon_image=logo_path)
st.markdown("<h2 style='color: orange;'>Kindly fill your information</h2>", unsafe_allow_html=True)

# Form styling
form_style = """
<div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; '>
    <h3 style='color: #333;'>Registration Form</h3>
"""

# with st.form(key="Registration"):
with st.form(key="Registration"):
    st.markdown(form_style, unsafe_allow_html=True)
    name = st.text_input("Name")
    course, section, year = st.columns(3, vertical_alignment="bottom")
    st.divider()
    
    with course:
        course = st.text_input("Course")
        
    with section:
        section = st.text_input("Section")
        
    with year:
        year = st.selectbox("Current Year", ["First", "Second", "Third", "Fourth"])
    
    st.divider()
    email = st.text_input("E-Mail Id")
    st.divider()
    phone = st.text_input("Phone Number")
    st.divider()
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    st.divider()
    interest = st.selectbox(
        "Which field are you interested in?",
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

df = pd.read_excel(file_path)

if submit_button:
    if email in df["E-mail"].values:
        st.warning(
            f"<h4 style='color: red;'>The email '{email}' is already registered. Please use a different email.</h4>",
            unsafe_allow_html=True
        )
    elif phone in df["Phone Number"].values:
        st.warning(
            f"<h4 style='color: red;'>The Phone Number '{phone}' is already registered. Please use a different phone number.</h4>",
            unsafe_allow_html=True
        )
    elif not name:
        st.markdown("<h4 style='color: red;'>Please enter your name...</h4>", unsafe_allow_html=True)
    elif not phone:
        st.markdown("<h4 style='color: red;'>Please enter your phone number...</h4>", unsafe_allow_html=True)
    elif not email:
        st.markdown("<h4 style='color: red;'>Please enter your email...</h4>", unsafe_allow_html=True)
    elif not gender:
        st.markdown("<h4 style='color: red;'>Please enter your gender...</h4>", unsafe_allow_html=True)
    elif not section:
        st.markdown("<h4 style='color: red;'>Please enter your section...</h4>", unsafe_allow_html=True)
    elif not year:
        st.markdown("<h4 style='color: red;'>Please enter your year...</h4>", unsafe_allow_html=True)
    elif not course:
        st.markdown("<h4 style='color: red;'>Please enter your course...</h4>", unsafe_allow_html=True)
    elif not interest:
        st.markdown("<h4 style='color: red;'>Please enter your interest...</h4>", unsafe_allow_html=True)
    else:
        if interest == "Others":
            interest = st.text_input("Enter your interest in 5-6 words at max")
        new_entry = pd.DataFrame(
            {
                "Name": [name],
                "Gender": [gender],
                "Section": [section],
                "Year": [year],
                "Course": [course],
                "E-mail": [email],
                "Phone Number": [phone],
                "Special/Interest": [interest],
            }
        )

        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(file_path, index=False)

        st.markdown(
            f"<h4 style='color: green;'>Thank you, {name}! Your registration has been successfully recorded.</h4>",
            unsafe_allow_html=True
        )
        thanks()
