# FAME Survey (Compact)

This repository contains:
- `fame_survey_compact.json` — compact survey repository (dimensions & questions).
- `streamlit_app.py` — a Streamlit app to run the survey.
- `FAME_questions_summary_by_dimension.csv` — counts by dimension.
- `FAME_questions_compact.csv` — the truncated question set used to build the JSON.

## How to run locally

```bash
pip install streamlit pandas
streamlit run streamlit_app.py
```
Ensure `fame_survey_compact.json` is in the same directory when you run the app.
