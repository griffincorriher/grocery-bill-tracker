import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from dataconnection import read_data


def grocery_bill_tracker():
    if st.button("Update worksheet"):    
        read_data()

    row = st.columns(3)
    st.title("Grocery Bill Tracker")
    st.sidebar.metric(label="MoM Spend", value=4, delta=-0.5, delta_color="inverse")
    st.sidebar.metric(label="YoY Spend", value=4, delta=-0.5, delta_color="inverse")

    with st.form("grocery_bill_form"):
        grocery_purchase_date = st.date_input("Grocery purchase date", datetime.now())
        grocery_bill = st.number_input("Grocery price", value=None, placeholder="Bill amount")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"Total spent this pay period:")
    
    return