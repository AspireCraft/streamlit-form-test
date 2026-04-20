import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Simple Enrolment Test", page_icon="📝", layout="centered")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_gsheet_client():
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(credentials)

def save_to_google_sheet(name, email, course):
    client = get_gsheet_client()
    sheet = client.open_by_key(st.secrets["https://docs.google.com/spreadsheets/d/1eLcyaSrqRfjHmo83F4bqtXtDq6aBAahZ7FGv4WHEnD8/edit?gid=0#gid=0"]["1eLcyaSrqRfjHmo83F4bqtXtDq6aBAahZ7FGv4WHEnD8"]).worksheet("Sheet1")
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        email,
        course,
    ])

st.title("Simple Enrolment Test Form")
st.write("Submit a test response and save it into Google Sheets.")

with st.form("test_form", clear_on_submit=True):
    name = st.text_input("Full name")
    email = st.text_input("Email")
    course = st.selectbox("Select course", ["Website Building", "Social Media Marketing", "Business Admin"])
    submitted = st.form_submit_button("Submit")

if submitted:
    if not name.strip() or not email.strip():
        st.error("Please fill in both name and email.")
    else:
        try:
            save_to_google_sheet(name.strip(), email.strip(), course)
            st.success("Saved to Google Sheets successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
