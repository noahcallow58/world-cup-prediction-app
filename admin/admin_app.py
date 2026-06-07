import json
import subprocess
import pandas as pd
import streamlit as st
from pathlib import Path

# Configure the page
st.set_page_config(page_title="World Cup Admin Panel", layout="wide")
st.title("World Cup 2026 Admin Dashboard")
st.subheader("Live Score Entry")

JSON_FILE = Path("ground_truth") / "worldcup_live.json"


# 1. Load the current JSON data
def load_schedule():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


if "schedule_data" not in st.session_state:
    st.session_state.schedule_data = load_schedule()

if "matches_df" not in st.session_state:
    df = pd.DataFrame(st.session_state.schedule_data["matches"])
    
    # Force score columns to nullable Int64 immediately so they aren't inferred as float64
    for col in ["team1_score", "team2_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            
    # Force dropdown fields to object dtype to safely handle string updates and None values
    for col in ["team1_live", "team2_live", "winner"]:
        if col in df.columns:
            df[col] = df[col].astype(object)
            
    st.session_state.matches_df = df

# Track the active phase to catch phase-switching events
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "Group Stage (Matchdays)"

# 2. Split into Group Stage and Knockouts for cleaner editing
st.write("### Filter Matches by Tournament Phase")
phase = st.radio(
    "Select Phase:",
    ["Group Stage (Matchdays)", "Knockout Rounds"],
    horizontal=True,
)

if phase != st.session_state.current_phase:
    if st.session_state.current_phase == "Group Stage (Matchdays)" and "group_edited_df" in st.session_state:
        df_to_merge = st.session_state.group_edited_df.copy()
        for col in ["team1_score", "team2_score"]:
            if col in df_to_merge.columns:
                df_to_merge[col] = pd.to_numeric(df_to_merge[col], errors="coerce").astype("Int64")
        
        st.session_state.matches_df.set_index("num", inplace=True)
        df_to_merge.set_index("num", inplace=True)
        for col in df_to_merge.columns:
            st.session_state.matches_df.loc[df_to_merge.index, col] = df_to_merge[col]
        st.session_state.matches_df.reset_index(inplace=True)
        
    elif st.session_state.current_phase == "Knockout Rounds" and "knockout_edited_df" in st.session_state:
        df_to_merge = st.session_state.knockout_edited_df.copy()
        for col in ["team1_score", "team2_score"]:
            if col in df_to_merge.columns:
                df_to_merge[col] = pd.to_numeric(df_to_merge[col], errors="coerce").astype("Int64")
                
        st.session_state.matches_df.set_index("num", inplace=True)
        df_to_merge.set_index("num", inplace=True)
        for col in df_to_merge.columns:
            st.session_state.matches_df.loc[df_to_merge.index, col] = df_to_merge[col]
        st.session_state.matches_df.reset_index(inplace=True)
    
    # Update the tracking state to the new phase
    st.session_state.current_phase = phase

# Dynamic Team List Extraction based on master data
matches_df = st.session_state.matches_df
group_matches = matches_df[matches_df["group"].notna()]
all_teams = sorted(
    list(set(group_matches["team1"].tolist() + group_matches["team2"].tolist()))
)

if phase == "Group Stage (Matchdays)":
    display_df = matches_df[matches_df["group"].notna()]
    columns_to_show = ["num", "round", "group", "team1", "team2", "team1_score", "team2_score"]

    st.write("#### Edit Match Details Below:")
    
    st.session_state.group_edited_df = st.data_editor(
        display_df[columns_to_show],
        hide_index=True,
        width="stretch",
        disabled=["num", "round", "group", "team1", "team2"],
        key="group_editor_widget"
    )

else:
    display_df = matches_df[matches_df["group"].isna()]
    columns_to_show = ["num", "round", "team1", "team2", "team1_live", "team2_live", "team1_score", "team2_score", "winner"]

    st.write("#### Edit Match Details Below:")
    st.info("Use the dropdown selections for live qualified teams and match winners to avoid spelling mistakes.")

    st.session_state.knockout_edited_df = st.data_editor(
        display_df[columns_to_show],
        hide_index=True,
        width='stretch',
        disabled=["num", "round", "team1", "team2"],
        column_config={
            "team1_live": st.column_config.SelectboxColumn("Team 1 (Live)", width="medium", options=all_teams, required=False),
            "team2_live": st.column_config.SelectboxColumn("Team 2 (Live)", width="medium", options=all_teams, required=False),
            "winner": st.column_config.SelectboxColumn("Official Winner", width="medium", options=all_teams, required=False),
        },
        key="knockout_editor_widget"
    )

if st.button("Save Changes & Update Scoreboard", type="primary"):
    # Ensure whatever is currently on screen gets merged into the master frame right before saving
    if phase == "Group Stage (Matchdays)" and "group_edited_df" in st.session_state:
        df_to_merge = st.session_state.group_edited_df.copy()
        for col in ["team1_score", "team2_score"]:
            if col in df_to_merge.columns:
                df_to_merge[col] = pd.to_numeric(df_to_merge[col], errors="coerce").astype("Int64")
        st.session_state.matches_df.set_index("num", inplace=True)
        df_to_merge.set_index("num", inplace=True)
        for col in df_to_merge.columns:
            st.session_state.matches_df.loc[df_to_merge.index, col] = df_to_merge[col]
        st.session_state.matches_df.reset_index(inplace=True)
        
    elif phase == "Knockout Rounds" and "knockout_edited_df" in st.session_state:
        df_to_merge = st.session_state.knockout_edited_df.copy()
        for col in ["team1_score", "team2_score"]:
            if col in df_to_merge.columns:
                df_to_merge[col] = pd.to_numeric(df_to_merge[col], errors="coerce").astype("Int64")
        st.session_state.matches_df.set_index("num", inplace=True)
        df_to_merge.set_index("num", inplace=True)
        for col in df_to_merge.columns:
            st.session_state.matches_df.loc[df_to_merge.index, col] = df_to_merge[col]
        st.session_state.matches_df.reset_index(inplace=True)

    # Convert back to JSON layout
    raw_matches = st.session_state.matches_df.to_dict(orient="records")
    clean_matches = []
    for match in raw_matches:
        clean_match = {}
        for k, v in match.items():
            if pd.isna(v):
                clean_match[k] = None
            elif k in ["team1_score", "team2_score"] and v is not None:
                clean_match[k] = int(v)
            else:
                clean_match[k] = v
        clean_matches.append(clean_match)

    st.session_state.schedule_data["matches"] = clean_matches

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.schedule_data, f, indent=2, ensure_ascii=False)

    st.success("Live scores updated.")

    with st.spinner("Recalculating user points..."):
        try:
            result = subprocess.run(["python", "scoreboard.py"], capture_output=True, text=True, check=True)
            st.code(result.stdout)
            st.success("Leaderboard updated!")
        except subprocess.CalledProcessError as e:
            st.error("Error executing scoreboard.py:")
            st.code(e.stderr)