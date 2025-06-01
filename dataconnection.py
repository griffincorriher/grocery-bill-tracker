import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Read secrets
spreadsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
worksheet = st.secrets["connections"]["gsheets"]["worksheet"]

def write_data(df):
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.update(
        worksheet=worksheet,
        data=df,
    )
    st.cache_data.clear()
    st.rerun()

def read_data():
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(
        spreadsheet=spreadsheet,
        worksheet=worksheet,
        usecols=[0, 1],
    )
    st.cache_data.clear()
    st.rerun()
    st.write(df)
    