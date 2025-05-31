import streamlit as st
import streamlit_authenticator as stauth
import datetime
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status'):
    with st.sidebar:
        authenticator.logout()


    row = st.columns(3)
    st.title("Grocery Bill Tracker")
    st.sidebar.metric(label="MoM Spend", value=4, delta=-0.5, delta_color="inverse")
    st.sidebar.metric(label="YoY Spend", value=4, delta=-0.5, delta_color="inverse")

    with st.form("grocery_bill_form"):
        grocery_purchase_date = st.date_input("Grocery purchase date", datetime.datetime.now())
        grocery_bill = st.number_input("Grocery price", value=None, placeholder="Bill amount")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"Total spent this pay period:")


elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')
