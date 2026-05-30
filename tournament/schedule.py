import json
from typing import List
import streamlit as st

from tournament.schemas import Group, Match, Team

# ------------------------------------------------------------
# Load data (cached so it doesn't reload every interaction)
# ------------------------------------------------------------
@st.cache_data
def load_groups():
    return load_openfootball_groups("data/worldcup.json")

def load_openfootball_groups(filepath: str):

    with open(filepath, "r") as f:
        data = json.load(f)

    matches_data = data.get("matches", [])

    groups = {}
    knockout_matches = []

    for i, m in enumerate(matches_data):

        group_name = m.get("group", "n/a")
        round = m.get("round")

        # ----------------------------------------------------
        # GROUP STAGE MATCH
        # ----------------------------------------------------
        match = Match(
            match_id=i + 1,
            home_team=Team(name=m["team1"]),
            away_team=Team(name=m["team2"]),
            home_ref=m["team1"] if group_name == "n/a" else None,
            away_ref=m["team2"] if group_name == "n/a" else None,
            round=round

        )

        # ----------------------------------------------------
        # GROUP STAGE
        # ----------------------------------------------------
        if group_name != "n/a":

            if group_name not in groups:
                groups[group_name] = []

            groups[group_name].append(match)

        # ----------------------------------------------------
        # KNOCKOUT STAGE
        # ----------------------------------------------------
        else:
            knockout_matches.append(match)

    group_objs = [
        Group(name=k, matches=v)
        for k, v in groups.items()
    ]

    return group_objs, knockout_matches

if __name__ == "__main__":

    groups = load_openfootball_groups("../data/worldcup.json")

    for group in groups:
        print(f"\n{group.name}")

        for match in group.matches:
            score = (
                f"{match.home_score}-{match.away_score}"
                if match.is_played()
                else "vs"
            )

            print(
                f"{match.match_id}: "
                f"{match.home_team.name} {score} {match.away_team.name}"
            )