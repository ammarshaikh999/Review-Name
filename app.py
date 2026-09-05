import re
import time
from io import StringIO

import pandas as pd
import streamlit as st
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.fakenamegenerator.com/gen-random-en-us.php"

# These values come from the supplied page source.
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

def make_email(name: str) -> str:
    local = re.sub(r"[^a-z0-9]", "", name.lower())
    return f"{local}@gmail.com"

def build_url(gender, name_set, country):
    g = {"Random": "random", "Male": "male", "Female": "female"}[gender]
    n = NAME_SETS[name_set]
    c = COUNTRIES[country]
    return f"https://www.fakenamegenerator.com/gen-{g}-{n}-{c}.php"

def generate(count, gender, name_set, country, progress, status):
    rows = []
    url = build_url(gender, name_set, country)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            for i in range(count):
                status.write(f"Generating {i + 1} / {count}...")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)

                # Supplied HTML shows the generated full name in .address h3.
                name_locator = page.locator(".info .address h3").first
                name = name_locator.inner_text(timeout=15000).strip()

                if not name:
                    raise RuntimeError("Generated name read nahi ho saka.")

                rows.append({"Name": name, "Email": make_email(name)})
                progress.progress((i + 1) / count)

                # Small courtesy delay between requests.
                if i + 1 < count:
                    time.sleep(0.5)
        finally:
            browser.close()

    return pd.DataFrame(rows)

st.set_page_config(page_title="Fake Name CSV Generator", page_icon="🧾", layout="centered")

st.title("🧾 Fake Name CSV Generator")
st.caption("Synthetic/test name data ko CSV mein export karein.")

with st.form("generator"):
    count = st.number_input("Number of names", min_value=1, max_value=500, value=10, step=1)
    gender = st.selectbox("Gender", ["Random", "Male", "Female"])
    name_set = st.selectbox("Name set", list(NAME_SETS.keys()), index=list(NAME_SETS).index("American"))
    country = st.selectbox("Country", list(COUNTRIES.keys()), index=list(COUNTRIES).index("United States"))
    submitted = st.form_submit_button("🚀 Generate CSV", use_container_width=True)

if submitted:
    progress = st.progress(0)
    status = st.empty()
    try:
        df = generate(int(count), gender, name_set, country, progress, status)
        st.success(f"{len(df)} names generate ho gaye.")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Download CSV",
            data=csv_bytes,
            file_name="generated_names.csv",
            mime="text/csv",
            use_container_width=True,
        )
        status.write("Done.")
    except Exception as exc:
        st.error(f"Error: {exc}")
        st.info("Agar website ka layout/URL change hua ho to scraper selectors update karne pad sakte hain.")

st.divider()
st.caption("Note: @gmail.com addresses synthetic text hain; tool Gmail accounts create nahi karta.")
