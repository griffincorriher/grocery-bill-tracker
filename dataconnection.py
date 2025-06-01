import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
# Read secrets
spreadsheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
worksheet = st.secrets["connections"]["gsheets"]["worksheet"]

df = pd.DataFrame()

def read_data():
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(
        spreadsheet=spreadsheet,
        worksheet=worksheet,
        usecols=[0, 1, 2],
    )

    df['pay period'] = pd.to_datetime(df['pay period']).dt.date
    df['grocery date'] = pd.to_datetime(df['grocery date']).dt.date


    return df
    # df_editor = st.data_editor(df, num_rows="dynamic")
    

def update_data(grocery_dict):
    temp_df = read_data()
    df = pd.concat([pd.DataFrame([grocery_dict]), temp_df], ignore_index=True)
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.update(
        worksheet=worksheet,
        data=df,
    )
    st.cache_data.clear()
    # st.rerun()


def refresh_data_table(grocery_dict):
    temp_df = read_data()
    df = pd.concat([pd.DataFrame([grocery_dict]), temp_df], ignore_index=True)
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.update(
        worksheet=worksheet,
        data=df,
    )
    st.cache_data.clear()
    st.rerun()

def clear_worksheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.clear(worksheet=worksheet)
    st.info("Worksheet Example 1 Cleared!")
    st.cache_data.clear()

    df = conn.update(
        worksheet=worksheet,
        data = pd.DataFrame({'grocery date': [],
                            'pay period': [],
                            'grocery bill': []}),
    )
    st.rerun()
