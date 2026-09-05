# Fake Name CSV Generator — Streamlit

GitHub + Streamlit-ready project.

## Local run

```bash
pip install -r requirements.txt
python -m playwright install chromium
streamlit run app.py
```

## Streamlit Cloud

1. Is repository ko GitHub par push karein.
2. Streamlit Community Cloud mein repository select karein.
3. Main file `app.py` select karein.
4. Deploy karein.

`packages.txt` aur `setup.sh` Chromium dependencies/install ke liye included hain.

## Features

- Count input
- Gender: Random / Male / Female
- Name set: page source mein available name sets
- Country: page source mein available countries
- CSV: Name + Email
- Email format: lowercase name without spaces/symbols + `@gmail.com`

The supplied page source shows the selector IDs `gen`, `n`, `c`, the Generate submit control, and the generated name under `.info .address h3`.

Use only for synthetic/test data and respect the target website's terms and rate limits.
