import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from dataconnection import update_data
import bisect
import yaml


def grocery_form():
    row = st.columns(3)
    st.title("Grocery Bill Tracker")
    st.sidebar.metric(label="MoM Spend", value=4, delta=-0.5, delta_color="inverse")
    st.sidebar.metric(label="YoY Spend", value=4, delta=-0.5, delta_color="inverse")

    grocery_dict = {}
    with st.form("grocery_bill_form", clear_on_submit=True):
        grocery_dict['grocery date'] = st.date_input("Grocery purchase date", datetime.now())

        with open("paydates.yaml", "r") as file:
            paydates_yaml = yaml.safe_load(file)

        paydates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in paydates_yaml["paydays"]])
        purchase_date = grocery_dict['grocery date']
        index = bisect.bisect_right(paydates, purchase_date) - 1
        if index >= 0:
            period_start = paydates[index]

        grocery_dict['pay period'] = period_start
        grocery_dict['grocery bill'] = st.number_input("Grocery price", value=None, placeholder="Bill amount")
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_data(grocery_dict)
            st.write(f"Total spent this pay period:")
            print('submitted')
    return