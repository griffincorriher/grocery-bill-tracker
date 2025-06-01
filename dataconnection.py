import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Read secrets
spreadsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
worksheet = st.secrets["connections"]["gsheets"]["worksheet"]

def write_data():

    st.title("Read Google Sheet as DataFrame")

    conn = st.connection("gsheets", type=GSheetsConnection)
    f = conn.read(worksheet="Example 1")

def read_data():
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(
        spreadsheet=spreadsheet,
        worksheet=worksheet,
        usecols=[0, 1],
    )

    st.write(df)
    