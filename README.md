# Fake Name CSV Generator — Streamlit

GitHub/Streamlit Cloud ke liye ready.

## Features

- Number of names
- Gender: Random / Male / Female
- Name set
- Country
- Name + generated `@gmail.com` text
- CSV preview
- CSV download

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

GitHub repository mein ye files upload karein aur Streamlit Community Cloud
mein `app.py` ko main file select karke deploy karein.

## Important

Is version mein Playwright/Chromium use nahi hota. Website ke generator ke
URL pattern ko directly request kiya jata hai, isliye `packages.txt` ki zarurat
nahi hai aur pehle wala `apt-get` dependency error nahi aayega.

The supplied page source shows that the site's Generate action changes the URL
to `/gen-{gender}-{name-set}-{country}.php`, and the generated name is in
`.info .address h3`.

Use only for synthetic/test data and respect the target website's terms and
rate limits.
