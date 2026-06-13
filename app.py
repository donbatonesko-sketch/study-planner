import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import math

# -------------------------
# CONFIG (mobilny widok)
# -------------------------

st.set_page_config(
    page_title="Smart Study Planner",
    layout="centered"
)

st.title("📘 Smart Study Planner")
st.write("Planowanie nauki + eksport do kalendarza 📅")

# -------------------------
# INPUT UI
# -------------------------

st.header("📥 Wprowadź materiał")

text = st.text_area("Wklej materiał do nauki", height=150)

st.header("⚙️ Ustawienia")

days = st.slider("Na ile dni rozłożyć naukę?", 1, 30, 5)

difficulty_mode = st.selectbox(
    "Poziom trudności",
    ["Łatwy", "Średni", "Trudny"]
)

# -------------------------
# FUNKCJA SZACOWANIA CZASU
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

    return math.ceil(base_time * multiplier)

# -------------------------
# FUNKCJA KALENDARZA (ICS)
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
        st.warning("Wklej najpierw materiał!")
        st.stop()

    sections = text.split("\n")
    sections = [s.strip() for s in sections if s.strip()]

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

    # -------------------------
    # EXPORT CSV
    # -------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Pobierz CSV",
        data=csv,
        file_name="plan_nauki.csv",
        mime="text/csv"
    )

    # -------------------------
    # EXPORT DO KALENDARZA
    # -------------------------

    ics = generate_ics(plan)

    st.download_button(
        label="📅 Dodaj do kalendarza (iPhone)",
        data=ics,
        file_name="plan_nauki.ics",
        mime="text/calendar"
    )

    # -------------------------
    # KALENDARZ VIEW
    # -------------------------

    st.header("🗓️ Widok dni")

    calendar = df.groupby("Data")["Temat"].apply(lambda x: " | ".join(x)).reset_index()

    for _, row in calendar.iterrows():
        st.write(f"📅 {row['Data']} → {row['Temat']}")