import streamlit as st
import pandas as pd
from tournament.knockout import (resolve_team, get_best_third_place_groups, get_annex_mapping)
from services.state import init_state

init_state()

def resolve_with_ui(ref, label, match_id, ref2):
    # Always let the engine look at group standings and knockout winners first
    result = resolve_team(ref, {
    "group_standings": st.session_state.group_standings,
    "knockout_winners": st.session_state.knockout_winners,
    "annex_mapping": st.session_state.get("annex_mapping", None),
    "knockout_losers": st.session_state.knockout_losers,
    }, ref2)

    # 1. If it's a standard string, everything resolved automatically
    if isinstance(result, str):
        return result

    # 2. Third place tie encountered
    if isinstance(result, dict) and result.get("type", "").endswith("THIRD_PLACE_TIE"):
        candidates = result["candidates"]
        
        # We tie the key strictly to the reset counter and match details
        suffix = f"rc_{st.session_state.reset_counter}"
        widget_key = f"widget_third_place_{match_id}_{label}_{suffix}"
        
        # Read a previously saved value if the user already clicked one
        past_choice = st.session_state.manual_tie_choices.get(widget_key)
        default_index = candidates.index(past_choice) if past_choice in candidates else 0

        chosen = st.selectbox(
            f"Resolve tied third place for {label.title()} Team",
            candidates,
            index=default_index,
            key=widget_key
        )
        
        # Save choice to a dedicated manual tracking state so the selectbox state sticks
        st.session_state.manual_tie_choices[widget_key] = chosen
        
        # CRITICAL: If your downstream resolve_team algorithm reads from placeholders 
        # like "W49", map this choice into st.session_state.knockout_winners or your state tree
        # so that subsequent matches can pick it up.
        # Example (Adjust the key to match what your backend layout expects):
        st.session_state.knockout_winners[f"MANUAL_{match_id}_{label}"] = chosen

        return chosen

    return "TBD"

def rebuild_annex_mapping():

    best_thirds = get_best_third_place_groups({
        "group_standings": st.session_state.group_standings
    })

    groups = [t["group"] for t in best_thirds]

    st.session_state.annex_mapping = get_annex_mapping(
        groups,
        st.session_state.annex_c
    )

st.title("Knockout Stage")

# ------------------------------------------------------------
# Initialize Missing Session States
# ------------------------------------------------------------
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if "manual_tie_choices" not in st.session_state:
    st.session_state.manual_tie_choices = {}

if "knockout_matches" not in st.session_state:
    st.warning("Knockout fixtures not initialised yet.")
    st.stop()

knockout_matches = st.session_state.knockout_matches

# ------------------------------------------------------------
# Reset Predictions Button
# ------------------------------------------------------------
if st.button("Reset Predictions"):
    st.session_state.knockout_winners = {}
    st.session_state.manual_tie_choices = {}

    for m in knockout_matches:
        m.home_score = 0
        m.away_score = 0

    st.session_state.reset_counter += 1

    # 🔥 ADD THIS
    rebuild_annex_mapping()

    st.rerun()

if (
    st.session_state.get("annex_mapping") is None
    and st.session_state.get("group_standings") is not None
):
    rebuild_annex_mapping()

winners = st.session_state.knockout_winners
losers = st.session_state["knockout_losers"]

# ------------------------------------------------------------
# 2. Render knockout matches
# ------------------------------------------------------------
# ------------------------------------------------------------
# Ensure Annex mapping is always consistent with group state
# ------------------------------------------------------------
if (
    st.session_state.get("group_standings") is not None
    and st.session_state.get("annex_c") is not None
):

    current_groups = set(
        t["group"]
        for t in get_best_third_place_groups({
            "group_standings": st.session_state.group_standings
        })
    )

    if (
        st.session_state.get("annex_mapping") is None
        or st.session_state.get("annex_groups") != current_groups
    ):
        st.session_state.annex_groups = current_groups
        rebuild_annex_mapping()

st.subheader("Knockout Fixtures")

if len(st.session_state["group_standings"]) != 12:
    st.error("Please complete group stage predictions.")

else:

    ROUND_ORDER = ["Round of 32", "Round of 16", "Quarter-final", "Semi-final", "Match for third place", "Final"]
    rounds = [r for r in ROUND_ORDER if any(m.round == r for m in knockout_matches)]
    selected_round = st.selectbox("Select Round", rounds)

    for match in knockout_matches:
        if match.round != selected_round:
            continue

        # Resolve teams dynamically based on state calculations
        home_team = resolve_with_ui(match.home_ref, "home", match.match_id, match.away_ref)
        away_team = resolve_with_ui(match.away_ref, "away", match.match_id, match.home_ref)

        match.home_team.name = home_team
        match.away_team.name = away_team

        st.markdown(f"### {home_team} vs {away_team}")
        col1, col2 = st.columns(2)
        
        suffix = f"rc_{st.session_state.reset_counter}"
        key = f"{match.match_id}_{suffix}"

        default_home = match.home_score if getattr(match, 'home_score', None) is not None else 0
        default_away = match.away_score if getattr(match, 'away_score', None) is not None else 0

        with col1:
            home_score = st.number_input(
                f"{home_team}",
                min_value=0,
                step=1,
                value=default_home,
                key=f"home_{key}",
            )

        with col2:
            away_score = st.number_input(
                f"{away_team}",
                min_value=0,
                step=1,
                value=default_away,
                key=f"away_{key}",
            )

        match.home_score = home_score
        match.away_score = away_score

        if home_score is not None and away_score is not None:
            if home_score > away_score:
                winner = home_team
                winners[f"W{match.match_id}"] = winner
                losers[f"L{match.match_id}"] = away_team
            elif away_score > home_score:
                winner = away_team
                winners[f"W{match.match_id}"] = winner
                losers[f"L{match.match_id}"] = home_team
            else:
                winner = st.selectbox(
                    "Winner after Penalties",
                    [home_team, away_team],
                    key=f"winner_{key}",
                )
                winners[f"W{match.match_id}"] = winner

                loser = away_team if winner == home_team else home_team
                losers[f"L{match.match_id}"] = loser

            match.winner = winner

    st.divider()