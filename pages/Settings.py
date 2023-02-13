import yaml
import os
import streamlit as st
import streamlit_authenticator as stauth

from utils import get_authenticator

authenticator, config = get_authenticator()

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.title('Settings')
    st.write(f"If you want to unsubscribe from TLRIA, please click the this link {os.environ['STRIPE_BILLING_URL']}")

    try:
        if authenticator.update_user_details(username, 'Update User Details'):
            with open('./auth.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)

    try:
        if authenticator.reset_password(username, 'Reset Password'):
            with open('./auth.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

    authenticator.logout('Logout', 'main')
