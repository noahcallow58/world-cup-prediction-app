# knockout.py

import re
from typing import Dict, Any


# ------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------
def resolve_team(ref: str, state: Dict[str, Any]):
    """
    Resolve a tournament reference into a team name.
    """

    if not ref:
        return None

    # --------------------------------------------------------
    # 1. Knockout winner reference (W74)
    # --------------------------------------------------------
    if ref.startswith("W"):
        return state["knockout_winners"].get(ref)

    # --------------------------------------------------------
    # 2. Group position reference (e.g. 1A, 2B)
    # --------------------------------------------------------
    if len(ref) == 2 and ref[0].isdigit():
        return resolve_group_position(ref, state)

    # --------------------------------------------------------
    # 3. Third-place pool (3A/B/C/D/F)
    # --------------------------------------------------------
    if ref.startswith("3") and "/" in ref:
        return resolve_best_third_place(ref, state)

    return ref


# ------------------------------------------------------------
# GROUP POSITION (1A, 2B)
# ------------------------------------------------------------
def resolve_group_position(ref: str, state: Dict[str, Any]):
    print(ref, state)
    pos = int(ref[0]) - 1
    group = ref[1]

    standings = state["group_standings"].get(group)

    if standings is None or len(standings) <= pos:
        return None

    return standings.iloc[pos]["Nation"]


# ------------------------------------------------------------
# BEST THIRD PLACE (3A/B/C/D/F)
# ------------------------------------------------------------
def resolve_best_third_place(ref: str, state: Dict[str, Any]):
    groups = ref[1:].split("/")  # A/B/C/D/F

    candidates = []

    for g in groups:
        df = state["group_standings"].get(g)

        if df is None or len(df) < 3:
            continue

        third_place = df.iloc[2]  # index 2 = 3rd place

        candidates.append({
            "team": third_place["Nation"],
            "Pts": third_place["Pts"],
            "GD": third_place["GD"],
            "GF": third_place["GF"],
        })

    if not candidates:
        return None

    # sort best third place
    best = sorted(
        candidates,
        key=lambda x: (x["Pts"], x["GD"], x["GF"]),
        reverse=True
    )[0]

    return best["team"]