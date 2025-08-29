
import json
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="FAME Survey", layout="wide")

@st.cache_data
def load_survey(path="fame_survey_compact.json"):
    with open(path, "r") as f:
        return json.load(f)

data = load_survey()

st.title(data["survey"]["title"])

scale = data["survey"]["scale"]
labels = scale.get("labels") or [str(i) for i in range(scale["min"], scale["max"]+1)]

responses = []
user_info = {}
with st.sidebar:
    st.header("Participant")
    user_info["name"] = st.text_input("Name", "")
    user_info["email"] = st.text_input("Email", "")
    user_info["role"] = st.text_input("Role/Function", "")
    user_info["org"] = st.text_input("Organization", "")

tabs = st.tabs([d["name"] for d in data["survey"]["dimensions"]])

for tab, dim in zip(tabs, data["survey"]["dimensions"]):
    with tab:
        st.subheader(dim["name"])
        for item in dim["questions"]:
            score = st.slider(f'{item["text"]}', min_value=scale["min"], max_value=scale["max"], value=int((scale["min"]+scale["max"])//2), key=item["id"])
            responses.append({"dimension": dim["name"], "question_id": item["id"], "question": item["text"], "score": score})

if st.button("Submit"):
    df = pd.DataFrame(responses)
    summary = df.groupby("dimension")["score"].mean().reset_index().rename(columns={"score":"avg_score"})
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_csv = f"fame_responses_{timestamp}.csv"
    out_summary = f"fame_summary_{timestamp}.csv"
    df.to_csv(out_csv, index=False)
    summary.to_csv(out_summary, index=False)
    st.success("Thank you! Your responses were recorded.")
    st.download_button("Download your detailed responses CSV", data=df.to_csv(index=False), file_name=out_csv, mime="text/csv")
    st.download_button("Download your dimension summary CSV", data=summary.to_csv(index=False), file_name=out_summary, mime="text/csv")

    st.write("### Dimension Averages")
    st.dataframe(summary)

    # --- Radar Chart (spider plot) of dimension averages ---
    st.write("### Radar Chart")
    categories = summary["dimension"].tolist()
    values = summary["avg_score"].tolist()
    if categories:
        # Close the loop for radar
        values += values[:1]
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig = plt.figure()  # single plot, no specific colors
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, values, linewidth=2)
        ax.fill(angles, values, alpha=0.1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticklabels([])
        ax.set_ylim(scale["min"], scale["max"])
        st.pyplot(fig)
