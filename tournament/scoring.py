import streamlit as st

def build_prediction_payload():

    groups = st.session_state.groups
    knockouts = st.session_state.knockout_matches


    # if st.secrets["env"]["environment"] == "dev":
    #     groups = groups[:2]  # Only Groups A and B

    # print(groups, st.secrets["env"]["environment"])

    missing = []
    predictions = []

    for group in groups:
        for match in group.matches:

            if not match.is_played():
                missing.append(
                    f"{group.name}: {match.home_team.name} vs {match.away_team.name}"
                )
                continue

            predictions.append({
                "match_id": match.match_id,
                "group": group.name,
                "home_team": match.home_team.name,
                "away_team": match.away_team.name,
                "home_score": match.home_score,
                "away_score": match.away_score,
            })

    if missing:
        st.error("Enter predictions for:\n" + "\n".join(missing))
        return []
    
    for knockout in knockouts:
        predictions.append({
            "match_id": knockout.match_id,
            "round": knockout.round,
            "home_team": knockout.home_team.name,
            "away_team": knockout.away_team.name,
            "home_score": knockout.home_score,
            "away_score": knockout.away_score,
            "winner": knockout.winner
        })

    return predictions