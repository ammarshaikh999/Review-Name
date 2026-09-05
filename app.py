import re
from io import BytesIO

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

BASE = "https://www.fakenamegenerator.com"

NAME_SETS = {
    "American": "us", "Arabic": "ar", "Australian": "au", "Brazil": "br",
    "Chechen (Latin)": "celat", "Chinese": "ch", "Chinese (Traditional)": "zhtw",
    "Croatian": "hr", "Czech": "cs", "Danish": "dk", "Dutch": "nl",
    "England/Wales": "en", "Eritrean": "er", "Finnish": "fi", "French": "fr",
    "German": "gr", "Greenland": "gl", "Hispanic": "sp", "Hobbit": "hobbit",
    "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Italian": "it",
    "Japanese": "jpja", "Japanese (Anglicized)": "jp", "Klingon": "tlh",
    "Ninja": "ninja", "Norwegian": "no", "Persian": "fa", "Polish": "pl",
    "Russian": "ru", "Russian (Cyrillic)": "rucyr", "Scottish": "gd",
    "Slovenian": "sl", "Swedish": "sw", "Thai": "th", "Vietnamese": "vn",
}

COUNTRIES = {
    "Australia": "au", "Austria": "as", "Belgium": "bg", "Brazil": "br",
    "Canada": "ca", "Cyprus (Anglicized)": "cyen", "Cyprus (Greek)": "cygk",
    "Czech Republic": "cz", "Denmark": "dk", "Estonia": "ee", "Finland": "fi",
    "France": "fr", "Germany": "gr", "Greenland": "gl", "Hungary": "hu",
    "Iceland": "is", "Italy": "it", "Netherlands": "nl", "New Zealand": "nz",
    "Norway": "no", "Poland": "pl", "Portugal": "pt", "Slovenia": "sl",
    "South Africa": "za", "Spain": "sp", "Sweden": "sw", "Switzerland": "sz",
    "Tunisia": "tn", "United Kingdom": "uk", "United States": "us",
    "Uruguay": "uy",
}

GENDERS = {"Random": "random", "Male": "male", "Female": "female"}

def make_url(gender, name_set, country):
    return (
        f"{BASE}/gen-{GENDERS[gender]}-{NAME_SETS[name_set]}-"
        f"{COUNTRIES[country]}.php"
    )

def make_email(name):
    local = re.sub(r"[^a-z0-9]", "", name.lower())
    return f"{local}@gmail.com"

@st.cache_resource
def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    })
    return s

def get_name(session, url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    node = soup.select_one(".info .address h3")
    if not node:
        raise RuntimeError("Generated name page par nahi mila.")
    return node.get_text(" ", strip=True)

st.set_page_config(page_title="Fake Name CSV Generator", page_icon="🧾")
st.title("🧾 Fake Name CSV Generator")
st.write("Synthetic/test names ko CSV mein generate karein.")

with st.form("settings"):
    count = st.number_input("Number of names", 1, 500, 10, 1)
    gender = st.selectbox("Gender", list(GENDERS))
    name_set = st.selectbox("Name set", list(NAME_SETS), index=list(NAME_SETS).index("American"))
    country = st.selectbox("Country", list(COUNTRIES), index=list(COUNTRIES).index("United States"))
    run = st.form_submit_button("🚀 Generate CSV", use_container_width=True)

if run:
    session = get_session()
    url = make_url(gender, name_set, country)
    rows = []
    progress = st.progress(0)
    status = st.empty()

    try:
        for i in range(int(count)):
            status.write(f"Generating {i + 1} / {int(count)}")
            name = get_name(session, url)
            rows.append({"Name": name, "Email": make_email(name)})
            progress.progress((i + 1) / int(count))

        df = pd.DataFrame(rows)
        st.success(f"{len(df)} names generate ho gaye.")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name="generated_names.csv",
            mime="text/csv",
            use_container_width=True,
        )
        status.write("Done.")
    except Exception as e:
        st.error(f"Generation error: {e}")
        st.info(
            "Target website ne request block ki ho sakti hai ya uska HTML layout "
            "change hua ho. Thori der baad dobara try karein."
        )

st.divider()
st.caption(
    "Note: @gmail.com addresses sirf synthetic/test text hain; "
    "ye tool Gmail accounts create nahi karta."
)
