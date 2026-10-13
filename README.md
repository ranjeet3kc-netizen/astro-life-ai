# Astro Life AI — Free Starter

A multilingual (Hindi, Nepali, English) Streamlit astrology website with:
- Sidereal Lahiri planetary positions
- Ascendant, Moon sign, Sun sign and whole-sign house mapping
- Career, money, love, marriage, health and life-phase reflection sections
- Varshphal 2027 month-by-month transit overview

## Important limitations
This is a starter version, not a complete professional Jyotish engine. Its 2027 section shows planetary sign snapshots around the 15th of each month and maps them to whole-sign houses from the birth ascendant. It is **not** a precise Tajika annual return chart and should not be presented as a guaranteed prediction. The health section is not medical advice.

## Files
- `app.py` — website
- `requirements.txt` — dependencies

## Deploy from an Android phone
1. Open GitHub in Chrome and sign in.
2. Tap **+** → **New repository**.
3. Name it `astro-life-ai`, choose **Public**, and tap **Create repository**.
4. In the repository, use **Add file** → **Create new file**.
5. Name the file `app.py`, paste the full code from this file, and commit it to `main`.
6. Add another file named `requirements.txt`, paste the contents from `requirements.txt`, and commit.
7. Open https://share.streamlit.io/ and sign in with GitHub.
8. Tap **Create app**, choose repository `astro-life-ai`, branch `main`, main file path `app.py`, then deploy.
9. Wait for installation to finish. If there is an error, open **Manage app → Logs** and share the exact error.

## Coordinates
Default location is Ghorahi, Nepal (approx. 27.6966 N, 82.4861 E). If the birth took place elsewhere, enter the correct latitude/longitude and local UTC offset. Nepal uses UTC+5:45 (5.75).
