import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import math
import re
from PyPDF2 import PdfReader

# -------------------------
# CONFIG (mobilny widok)
# -------------------------

st.set_page_config(
    page_title="Smart Study Planner",
    layout="centered"
)

st.title("📘 Smart Study Planner")
st.write("Planowanie nauki z PDF + kalendarz 📅")

# -------------------------
# WGRYWANIE PDF
# -------------------------

st.header("📥 Wgraj materiał")

uploaded_file = st.file_uploader("Wrzuć PDF", type=["pdf"])

text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    
    for page in reader.pages:
        if page.extract_text():
