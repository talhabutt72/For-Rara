# Miles Apart — a little gift world

## How to personalize (do this first!)
Open `app.py`, scroll to the `CONFIG` dict at the very top, and edit:
- `her_name` — currently "Rara"
- `inside_jokes` — add your real ones, used in The Talo Times

## Add your handwriting letter
Photograph each page, name them `01.jpg`, `02.jpg`, `03.jpg`... and drop
them into `assets/handwriting/`. They'll appear automatically, in order,
on the "Handwritten For You" page.

## Run it locally
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free (Streamlit Community Cloud)
1. Push this folder to a GitHub repo.
2. Go to share.streamlit.io, connect the repo, deploy `app.py`.
3. Once she opens the link on her iPhone Safari, she can tap
   Share -> "Add to Home Screen" so it opens like a real app, no browser bars.

No API key needed — everything (complaint letters, headlines, guesses)
is pre-written and randomized locally, so it works instantly, every time.
