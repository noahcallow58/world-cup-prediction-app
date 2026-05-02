import streamlit as st
import json

st.set_page_config(page_title="World Cup Charity Challenge", page_icon="🏆")

st.title("🏆 World Cup Charity Challenge")

st.write("Predict the scores for two matches. The winners will advance to the final!")

# Helper function
def determine_winner(team1, score1, team2, score2):
    if score1 > score2:
        return team1
    elif score2 > score1:
        return team2
    else:
        return "TBD (Draw - choose manually)"

# Prediction form
with st.form("prediction_form"):

    name = st.text_input("Your Name")

    st.subheader("Semi-Final 1")
    sf1_team1 = "France"
    sf1_team2 = "Brazil"
    sf1_score1 = st.number_input(f"{sf1_team1} Score", min_value=0, step=1)
    sf1_score2 = st.number_input(f"{sf1_team2} Score", min_value=0, step=1)

    st.subheader("Semi-Final 2")
    sf2_team1 = "England"
    sf2_team2 = "Germany"
    sf2_score1 = st.number_input(f"{sf2_team1} Score", min_value=0, step=1)
    sf2_score2 = st.number_input(f"{sf2_team2} Score", min_value=0, step=1)

    # Determine winners
    finalist1 = determine_winner(sf1_team1, sf1_score1, sf1_team2, sf1_score2)
    finalist2 = determine_winner(sf2_team1, sf2_score1, sf2_team2, sf2_score2)

    st.subheader("Final")

    if "TBD" in finalist1 or "TBD" in finalist2:
        st.warning("A draw was predicted in a semi-final. Please select finalists manually.")

        finalist1 = st.selectbox(
            "Choose Finalist 1",
            [sf1_team1, sf1_team2]
        )

        finalist2 = st.selectbox(
            "Choose Finalist 2",
            [sf2_team1, sf2_team2]
        )

    st.write(f"🏁 Final Match: **{finalist1} vs {finalist2}**")

    final_score1 = st.number_input(f"{finalist1} Final Score", min_value=0, step=1)
    final_score2 = st.number_input(f"{finalist2} Final Score", min_value=0, step=1)

    submit = st.form_submit_button("Generate Entry File")

# Output + download
if submit:

    prediction_data = {
        "name": name,
        "semi_finals": {
            "France_vs_Brazil": {
                "France": sf1_score1,
                "Brazil": sf1_score2,
                "winner": finalist1
            },
            "England_vs_Germany": {
                "England": sf2_score1,
                "Germany": sf2_score2,
                "winner": finalist2
            }
        },
        "final": {
            "match": f"{finalist1} vs {finalist2}",
            finalist1: final_score1,
            finalist2: final_score2
        }
    }

    json_string = json.dumps(prediction_data, indent=4)

    st.success("Entry Generated! Download your prediction file below.")

    st.download_button(
        label="💾 Download Entry.json",
        data=json_string,
        file_name=f"{name.replace(' ', '_')}_entry.json",
        mime="application/json"
    )