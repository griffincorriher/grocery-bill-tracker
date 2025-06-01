import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from grocery_bill_tracker import grocery_bill_tracker
from paydaysapi import get_semi_monthly_paydays, save_to_yaml
import os
from datetime import datetime

if (datetime.now().month == 1 and datetime.now().day == 1) or not os.path.exists("paydays.yaml"):
    print(f"pay year: {datetime.now().year}")
    paydates = get_semi_monthly_paydays(datetime.now().year)
    save_to_yaml(paydates)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)


try:
    authenticator.login()

except Exception as e:
    st.error(e)


if st.session_state.get('authentication_status'):
    if 'avatar' not in st.session_state:
        st.session_state['avatar'] = config['credentials']['usernames'][st.session_state['username']]['avatar']

    spacer, user_block = st.columns([6, 4])

    with user_block:
        name_col, logout_col = st.columns([4, 2])  # Adjust these as needed

        with name_col:
            st.markdown(f"<div style='margin-top: 8px;'>{st.session_state['avatar']} {st.session_state['username']}</div>", unsafe_allow_html=True)

        with logout_col:
            authenticator.logout("Logout", location="main")

    grocery_bill_tracker()

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')

if not st.session_state.get('authentication_status'):
    st.session_state.pop("avatar", None)