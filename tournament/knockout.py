# knockout.py

import re
from typing import Dict, Any
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------
def resolve_team(ref: str, state: Dict[str, Any], ref2: str):

    if not ref:
        return None

    # 1. Knockout winner reference
    if ref.startswith("W"):
        return state["knockout_winners"].get(ref)
    
    elif ref.startswith("L"):
        return state["knockout_losers"].get(ref)

    # 2. Group position reference (1A, 2B)
    elif len(ref) == 2 and ref[0].isdigit():
        return resolve_group_position(ref, state)

    elif ref.startswith("3"):
        
        annex_c = st.session_state.annex_c

        best_thirds = get_best_third_place_groups(state)
        best_groups = sorted([t["group"] for t in best_thirds])
        
        

        # if ("cached_best_third_groups" not in st.session_state
        #     or st.session_state.cached_best_third_groups != best_groups):
        
            # st.session_state.cached_best_third_groups = best_groups
        # print("\nQualified third-place teams:")
        # for team in best_thirds:
        #     print(
        #         f"{team['group']} -> {team['team']} "
        #         f"(Pts={team['Pts']}, GD={team['GD']}, GF={team['GF']})"
        #     )
            
        # print("\nBest third-place groups:")
        # print(best_groups)

        mapping = get_annex_mapping(best_groups, annex_c)
        # print(mapping)
        

        return resolve_group_position(mapping[ref2], state)

    return ref


# ------------------------------------------------------------
# GROUP POSITION (1A, 2B)
# ------------------------------------------------------------
def resolve_group_position(ref: str, state: Dict[str, Any]):

    pos = int(ref[0]) - 1
    group = ref[1]

    standings = state["group_standings"].get(group)

    if standings is None or len(standings) <= pos:
        return None

    return standings.iloc[pos]["Nation"]

# ------------------------------------------------------------
# BEST THIRD PLACE (3A/B/C/D/F)
# ------------------------------------------------------------
def get_best_third_place_groups(state):

    thirds = []

    for group, df in state["group_standings"].items():

        if len(df) < 3:
            continue

        third = df.iloc[2]

        thirds.append({
            "group": group,
            "team": third["Nation"],
            "Pts": third["Pts"],
            "GD": third["GD"],
            "GF": third["GF"],
        })

    thirds.sort(
        key=lambda x: (x["Pts"], x["GD"], x["GF"]),
        reverse=True
    )

    return thirds[:8]

def parse_annex_row(row):
    return {
        "1A": row["1A"],
        "1B": row["1B"],
        "1D": row["1D"],
        "1E": row["1E"],
        "1G": row["1G"],
        "1I": row["1I"],
        "1K": row["1K"],
        "1L": row["1L"],
    }

def get_annex_mapping(best_groups, annex_df):

    target = set(best_groups)

    bp_cols = [c for c in annex_df.columns if c.startswith("BP")]

    for _, row in annex_df.iterrows():

        groups = {
            str(x).strip()
            for x in row[bp_cols]
            if pd.notna(x)
        }

        if groups == target:
            return parse_annex_row(row)

    return None

if __name__ == "__main__":

    annex_c = pd.read_csv("/Users/noahcallow/Documents/Python/WorldCupApp/world-cup-prediction-app/data/annexC.csv")

    # Mock group standings
    state = {
        "group_standings": {
            "A": pd.DataFrame([
                {"Nation": "A1", "Pts": 9, "GD": 5, "GF": 8},
                {"Nation": "A2", "Pts": 6, "GD": 2, "GF": 5},
                {"Nation": "A3", "Pts": 1, "GD": -2, "GF": 2},
            ]),
            "B": pd.DataFrame([
                {"Nation": "B1", "Pts": 9, "GD": 6, "GF": 9},
                {"Nation": "B2", "Pts": 4, "GD": 0, "GF": 4},
                {"Nation": "B3", "Pts": 2, "GD": -1, "GF": 3},
            ]),
            "C": pd.DataFrame([
                {"Nation": "C1", "Pts": 7, "GD": 3, "GF": 6},
                {"Nation": "C2", "Pts": 5, "GD": 1, "GF": 5},
                {"Nation": "C3", "Pts": 1, "GD": -3, "GF": 2},
            ]),
            "D": pd.DataFrame([
                {"Nation": "D1", "Pts": 7, "GD": 4, "GF": 7},
                {"Nation": "D2", "Pts": 5, "GD": 1, "GF": 4},
                {"Nation": "D3", "Pts": 4, "GD": 0, "GF": 4},
            ]),
            "E": pd.DataFrame([
                {"Nation": "E1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "E2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "E3", "Pts": 5, "GD": 2, "GF": 5},
            ]),
            "F": pd.DataFrame([
                {"Nation": "F1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "F2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "F3", "Pts": 5, "GD": 1, "GF": 5},
            ]),
            "G": pd.DataFrame([
                {"Nation": "G1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "G2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "G3", "Pts": 5, "GD": 0, "GF": 5},
            ]),
            "H": pd.DataFrame([
                {"Nation": "H1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "H2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "H3", "Pts": 4, "GD": 1, "GF": 4},
            ]),
            "I": pd.DataFrame([
                {"Nation": "I1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "I2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "I3", "Pts": 4, "GD": 0, "GF": 4},
            ]),
            "J": pd.DataFrame([
                {"Nation": "J1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "J2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "J3", "Pts": 4, "GD": -1, "GF": 4},
            ]),
            "K": pd.DataFrame([
                {"Nation": "K1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "K2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "K3", "Pts": 4, "GD": -2, "GF": 4},
            ]),
            "L": pd.DataFrame([
                {"Nation": "L1", "Pts": 9, "GD": 5, "GF": 9},
                {"Nation": "L2", "Pts": 6, "GD": 2, "GF": 6},
                {"Nation": "L3", "Pts": 4, "GD": -3, "GF": 4},
            ]),
        }
    }

    best_thirds = get_best_third_place_groups(state)

    print("\nQualified third-place teams:")
    for team in best_thirds:
        print(
            f"{team['group']} -> {team['team']} "
            f"(Pts={team['Pts']}, GD={team['GD']}, GF={team['GF']})"
        )

    best_groups = sorted([t["group"] for t in best_thirds])

    print("\nBest third-place groups:")
    print(best_groups)

    mapping = get_annex_mapping(best_groups, annex_c)

    print("\nAnnex C row:")
    print(mapping)