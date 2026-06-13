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
# PDF UPLOAD (POPRAWIONY)
# -------------------------

st.header("📥 Wgraj materiał (PDF)")

uploaded_file = st.file_uploader(
    "📄 Kliknij i wybierz plik PDF",
    type=["pdf"]
)

text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.success(f"✅ Wczytano plik: {uploaded_file.name}")

# -------------------------
# ALTERNATYWA — TEKST RĘCZNY
# -------------------------

st.header("✍️ Lub wklej tekst")

manual_text = st.text_area("Wklej materiał", height=150)

if manual_text:
    text = manual_text

# -------------------------
# USTAWIENIA
# -------------------------

st.header("⚙️ Ustawienia")

days = st.slider("Na ile dni rozłożyć naukę?", 1, 30, 5)

difficulty_mode = st.selectbox(
    "Poziom trudności",
    ["Łatwy", "Średni", "Trudny"]
)

# -------------------------
# SZACOWANIE CZASU
# -------------------------

def estimate_time(section, difficulty):
    words = len(section.split())
    base_time = words / 200

    if difficulty == "Łatwy":
        multiplier = 1
    elif difficulty == "Średni":
        multiplier = 1.5
    else:
        multiplier = 2

    return max(1, math.ceil(base_time * multiplier))

# -------------------------
# KALENDARZ (ICS)
# -------------------------

def generate_ics(plan):
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\n"

    for event in plan:
        date = datetime.strptime(event["Data"], "%Y-%m-%d")

        start = date.strftime("%Y%m%dT090000")
        end = date.strftime("%Y%m%dT100000")

        ics_content += f"""BEGIN:VEVENT
SUMMARY:{event['Temat']}
DTSTART:{start}
DTEND:{end}
DESCRIPTION:Nauka - Smart Planner
END:VEVENT
"""

    ics_content += "END:VCALENDAR"
    return ics_content

# -------------------------
# GENEROWANIE PLANU
# -------------------------

if st.button("🚀 Generuj plan nauki", use_container_width=True):

    if not text.strip():
        st.warning("Najpierw wgraj PDF lub wklej tekst!")
        st.stop()

    # 🔥 podział tekstu (pseudo AI)
    sections = re.split(r'\n|\. ', text)
    sections = [s.strip() for s in sections if len(s.strip()) > 50]

    if len(sections) == 0:
        st.warning("Nie udało się podzielić materiału.")
        st.stop()

    plan = []
    start_date = datetime.today()

    for i, section in enumerate(sections):
        day = start_date + timedelta(days=i % days)
        time_estimate = estimate_time(section, difficulty_mode)

        plan.append({
            "Data": day.strftime("%Y-%m-%d"),
            "Temat": section,
            "Szacowany czas (min)": time_estimate
        })

    df = pd.DataFrame(plan)

    # -------------------------
    # OUTPUT
    # -------------------------

    st.header("📅 Twój plan")

    st.dataframe(df, use_container_width=True)

    total_time = df["Szacowany czas (min)"].sum()
    st.info(f"⏱️ Łączny czas: {total_time} min (~{round(total_time/60,1)} h)")

    # CSV

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Pobierz CSV",
        data=csv,
        file_name="plan_nauki.csv",
        mime="text/csv"
    )

    # KALENDARZ

    ics = generate_ics(plan)

    st.download_button(
        label="📅 Dodaj do kalendarza (iPhone)",
        data=ics,
        file_name="plan_nauki.ics",
        mime="text/calendar"
    )

    # WIDOK DNIA

    st.header("🗓️ Widok dni")

    calendar = df.groupby("Data")["Temat"].apply(lambda x: " | ".join(x)).reset_index()

    for _, row in calendar.iterrows():
        st.write(f"📅 {row['Data']} → {row['Temat']}")
