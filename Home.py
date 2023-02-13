import yaml
import time
import base64
import uuid
import streamlit as st
import streamlit_authenticator as stauth

from utils import get_text_from_url, get_text_from_pdf, auth_layer
from model import summarize

st.set_page_config(
    page_title="SaoS",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "mailto:example@example.com",
        "Report a bug": "mailto:example@example.com",
        "About": "# SaoS. Streamlit Complete Web App."
    }
)


def home():
    st.title("Welcome to Saos")
    col1, col2 = st.columns(2)
    with col1:
        selectbox = st.selectbox("Raw Text, PDF or URL source", ("URL", "Raw Text", "PDF"))
        if selectbox == "Raw Text":
            text = st.text_area("Provide here the text you want to summarize", value="", height=300)

        if selectbox == "PDF":
            uploaded_file = st.file_uploader("Choose a PDF file to summarize", type=["pdf"])
            if uploaded_file is not None:
                bytes_data = uploaded_file.read()
                file_path = f'./data/{str(uuid.uuid4())[:8]}.{uploaded_file.name[-3:]}'

                with open(file_path, 'wb') as f:
                    f.write(bytes_data)

                if uploaded_file.name[-3:] == "pdf":
                    with open(file_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)

        if selectbox == "URL":
            url = st.text_input("Provide a URL you want to summarize", value="")

        button = st.button("Summarize")

    with col2:
        if button:
            with st.spinner("Wait for it..."):
                if selectbox == "URL":
                    text = get_text_from_url(url)
                elif selectbox == "PDF":
                    text = get_text_from_pdf(file_path)
                st.text_area(label="Summary", value=summarize(text), height=300)


auth_layer(home)
