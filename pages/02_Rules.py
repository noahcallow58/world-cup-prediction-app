import streamlit as st
from services.state import init_state

# Initialize session state across pages
init_state()

st.title("Competition Rules")

st.markdown("""
Welcome to the World Cup Prediction Competition. 
Please read the rules carefully before submitting your predictions.
""")

# --------------------------------------------------
# 1. GENERAL & ENTRY RULES
# --------------------------------------------------
st.header("Entry Rules")

st.markdown("""
- Enter your name and e-mail address on the submission form.
- Predict the score of **every match**.
- Select your predicted progression paths all the way to the Tournament Winner.
- Ensure all predictions are completed before submission.
- Entry fee: **£5 per entry** (No payment = no valid entry).
- Competition placings will be e-mailed to entrants who provide a valid e-mail address.
""")

st.error(
    "Final group placings will be taken from the official FIFA website. "
)

# --------------------------------------------------
# 2. SCORING SYSTEM
# --------------------------------------------------
st.header("Scoring System")

st.info(
    "**Stay Engaged!** In order to retain everybody's interest in the latter stages of the competition, "
    "points can still be gained for correct scores and outcomes even if your chosen teams are no longer in "
    "the competition. You just get extra bonus points if you have chosen the correct teams to progress!"
)

# Organize the complex scoring rules cleanly using Streamlit Tabs
tab1, tab2, tab3 = st.tabs(["Base Match Points", "Group Stage Bonuses", "Knockout Stage Bonuses"])

with tab1:
    st.subheader("Points Available per Match")
    st.markdown("""
    The baseline scoring system applies to **every single match** across the entire tournament:
    
    * **3 points** for selecting the exact correct match score.
    * **2 points** for selecting the correct outcome (*Home Win, Away Win, or Draw*).
    * **2 points per team** for correctly predicting their specific goals scored (*Up to 4 points total*).
    
    **Maximum points per game: 9 points**
    """)

with tab2:
    st.subheader("Group Standings Bonus Points")
    st.markdown("""
    At the conclusion of the group stage, you will receive:
    
    * **5 Bonus points** for selecting a correct Group Winner.
    * **5 Bonus points** for selecting a correct Group Runner-Up.
    * **5 Bonus points** for selecting a correct 3rd Placed Team.
    """)

with tab3:
    st.subheader("Knockout Progression Bonuses")
    st.markdown("""
    Every knockout match scores base points identically to Round 1, but carries varying team advancement bonuses:
    
    * **Round 2 (Round of 32):** **5 Bonus points** for selecting the winners.
    * **Round 3 (Round of 16):** **5 Bonus points** for selecting the winners.
    * **Quarter Finals:** **10 Bonus points** for selecting the winners (*Semi Finalists*).
    * **Semi Finals:** **15 Bonus points** for selecting the winners (*Finalists*).
    * **Final:** **20 Bonus points** for selecting the correct Tournament Winner.
    """)
    
    st.warning(
        "**Knockout Score Rule:** The final score after the completion of **NORMAL TIME + EXTRA TIME** "
        "will be used for match score calculations. Penalty shootouts will *only* be used to determine "
        "which team officially advances for your progression bonus points."
    )

# --------------------------------------------------
# 3. PRIZES
# --------------------------------------------------
st.header("Prizes")

st.markdown("""
Prizes will be calculated once all tournament entry monies have been collected. 
Prizes will be officially issued to the top configurations only:

* **1st Place**
* **2nd Place**
* **3rd Place**
""")

st.caption("A portion of the proceeds will be set aside as a donation to **Prostate Cancer Research**.")

# --------------------------------------------------
# 4. ADDITIONAL RULES
# --------------------------------------------------
st.header("Additional Rules")

st.markdown("""
1. Somebody **must** be worse at predicting the results than the organiser. It is the law.
2. All participants must do their absolute best to beat my best mate **Mike Green** (*That's Mike Green, Everybody!*).
3. The most important rule of all: **have fun!**
""")