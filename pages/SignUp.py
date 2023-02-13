import yaml
import streamlit as st
import streamlit_authenticator as stauth

from utils import get_authenticator

authenticator, config = get_authenticator()


try:
    if authenticator.register_user("Register user", preauthorization=False):
        with open("./auth.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        st.success("User registered successfully")
except Exception as e:
    st.error(e)
