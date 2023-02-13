import os
import yaml
import stripe
import time
import random
import requests
import redis

import streamlit as st
import streamlit_authenticator as stauth

from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",]

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)


def get_config():
    with open("./auth.yaml") as file:
        config = yaml.safe_load(file)
    return config


def get_authenticator():
    config = get_config()
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"]
    )
    return authenticator, config


def check_subscription(email):
    customers = stripe.Customer.list()["data"]
    customers_emails = [customer["email"] for customer in customers]
    return email in customers_emails


def get_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    document = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        document = document + text
    return document.replace("\n", " ")


def get_text_from_url(url):
    agent = AGENTS[random.randint(0, len(AGENTS) - 1)]
    response = requests.get(url, headers={"User-Agent": agent, "Connection": "close"})
    soup = BeautifulSoup(response.text, "html.parser")
    elements = [
        element.text for element in soup.find_all(["h1", "h2", "h3", "p"])
        if len(element.text) > 5
    ]
    return "\n\n".join(elements)[:6000].strip().replace("\n", " ")


def auth_layer(page):
    authenticator, config = get_authenticator()

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status is None:
        st.warning("Please Enter your Username and Password")
        st.write(f"Dont have an account? Register here {os.environ['CUSTOM_DOMAIN']}/SignUp")
    if authentication_status is False:
        st.error("Username/password is Incorrect")
    elif authentication_status:
        email = config["credentials"]["usernames"][username]["email"]
        if check_subscription(email) is False:
            st.title("Welcome to TLRIA")
            st.write("In order to use TLRIA, you need to subscribe to our service. Please click on the button below to subscribe.")
            st.warning("Please note that you will be redirected to a third party website.")
            st.write(f"You can subscribe here: {os.environ['STRIPE_PAYMENT_URL']}")
            st.warning("Make sure you provide the same email address you used to register to TLRIA.")
        else:
            page()
