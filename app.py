import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import math
import re
from PyPDF2 import PdfReader

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Smart Study Planner",
    layout="centered"
)

st.title("📘 Smart Study Planner")
st.write("Planowanie nauki z PDF + kalendarz 📅")

# -------------------------
# PDF UPLOAD
# -------------------------

st.header("📥 Wgraj materiał (PDF)")

uploaded_file = st.file_uploader("Wrzuć PDF", type=["pdf"])

text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
