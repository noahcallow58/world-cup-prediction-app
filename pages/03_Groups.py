import streamlit as st
import pandas as pd

from tournament.schedule import load_openfootball_groups

# ------------------------------------------------------------
# Load data (cached so it doesn't reload every interaction)
# ------------------------------------------------------------
@st.cache_data
def load_groups():
    return load_openfootball_groups("data/worldcup.json")


groups = load_groups()


# ------------------------------------------------------------
# Session state for predictions
# ------------------------------------------------------------
# if "predictions" not in st.session_state:
#     st.session_state.predictions = {}


st.title("Group Stage Predictions")


# ------------------------------------------------------------
# Group selector (A–L)
# ------------------------------------------------------------
group_names = [g.name for g in groups]

selected_group_name = st.selectbox("Select Group", group_names)

group = next(g for g in groups if g.name == selected_group_name)

st.subheader(f"Group {group.name}")
st.divider()


# ------------------------------------------------------------
# Helper: update prediction state
# ------------------------------------------------------------
def set_prediction(match_id: int, home: int, away: int):
    st.session_state.predictions[f"{match_id}_home"] = home
    st.session_state.predictions[f"{match_id}_away"] = away


# ------------------------------------------------------------
# 1. Prediction Input Section
# ------------------------------------------------------------
st.markdown("## Predictions")

for match in group.matches:

    st.markdown(
        f"### {match.home_team.name} vs {match.away_team.name}"
    )

    col1, col2 = st.columns(2)

    key_home = f"{match.match_id}_home"
    key_away = f"{match.match_id}_away"

    default_home = st.session_state.predictions.get(key_home, 0)
    default_away = st.session_state.predictions.get(key_away, 0)

    with col1:
        home_score = st.number_input(
            f"{match.home_team.name}",
            min_value=0,
            step=1,
            value=default_home,
            key=f"input_{key_home}",
        )

    with col2:
        away_score = st.number_input(
            f"{match.away_team.name}",
            min_value=0,
            step=1,
            value=default_away,
            key=f"input_{key_away}",
        )

    set_prediction(match.match_id, home_score, away_score)

    st.divider()


# ------------------------------------------------------------
# 2. Standings Calculation (derived state)
# ------------------------------------------------------------
st.markdown("## Standings")


def compute_standings(group):

    table = {}

    for match in group.matches:

        if match.match_id not in [int(k.split("_")[0]) for k in st.session_state.predictions.keys()]:
            continue

        home_goals = st.session_state.predictions.get(f"{match.match_id}_home", 0)
        away_goals = st.session_state.predictions.get(f"{match.match_id}_away", 0)

        for team in [match.home_team.name, match.away_team.name]:
            if team not in table:
                table[team] = {
                    "MP": 0,
                    "W": 0,
                    "D": 0,
                    "L": 0,
                    "GF": 0,
                    "GA": 0,
                    "Pts": 0,
                }

        home = table[match.home_team.name]
        away = table[match.away_team.name]

        home["MP"] += 1
        away["MP"] += 1

        home["GF"] += home_goals
        home["GA"] += away_goals

        away["GF"] += away_goals
        away["GA"] += home_goals

        if home_goals > away_goals:
            home["W"] += 1
            away["L"] += 1
            home["Pts"] += 3

        elif home_goals < away_goals:
            away["W"] += 1
            home["L"] += 1
            away["Pts"] += 3

        else:
            home["D"] += 1
            away["D"] += 1
            home["Pts"] += 1
            away["Pts"] += 1

    # convert to dataframe
    df = pd.DataFrame.from_dict(table, orient="index")
    df["GD"] = df["GF"] - df["GA"]

    df = df.sort_values(
        by=["Pts", "GD", "GF"],
        ascending=False,
    )

    df.index.name = "Nation"
    df = df.reset_index()

    # Insert position column
    df.insert(0, "", range(1, len(df) + 1))
    return df


standings_df = compute_standings(group)

st.dataframe(standings_df, width='stretch', hide_index=True)


# ------------------------------------------------------------
# 3. Qualification preview
# ------------------------------------------------------------
st.markdown("## Qualification (Preview)")

top2 = standings_df.head(2)

st.write("### Top 2")
st.dataframe(top2, hide_index=True)