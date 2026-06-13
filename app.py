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

