import streamlit as st
from services.state import init_state

init_state()


st.title("Competition Rules")

st.markdown("""
Welcome to the World Cup Prediction Competition.

Please read the rules carefully before submitting your predictions.
""")

# --------------------------------------------------
# ENTRY RULES
# --------------------------------------------------
st.header("Entry Rules")

st.markdown("""
- Enter your name and e-mail address on the submit form.
- Predict the score of every match.
- Select:
    - Group Winners
    - Group Runners-Up
    - Quarter Finalists
    - Semi Finalists
    - Finalists
    - Tournament Winner
- Ensure all predictions are completed before submission.
- Entry fee: **£5 per entry**.
- No payment = no valid entry.
- Competition placings will be e-mailed to entrants who provide a valid e-mail address.
""")

st.warning(
    "Once the tournament starts, predictions cannot be modified."
)

# --------------------------------------------------
# SCORING
# --------------------------------------------------
st.header("Scoring System")

st.info(
    "Points can still be earned throughout the knockout stages even if your chosen teams have been eliminated."
)

# --------------------------------------------------
# GROUP STAGE
# --------------------------------------------------
st.subheader("Group Stage Matches")

st.markdown("""
For each match:

- **3 points** for the exact score.
- **2 points** for correctly predicting the match outcome:
    - Home Win
    - Away Win
    - Draw
- **2 points per team score correctly predicted**
    - Home team goals correct = 2 points
    - Away team goals correct = 2 points

**Maximum: 9 points per match**
""")

st.subheader("Group Standings")

st.markdown("""
Bonus points:

- **5 points** for each correctly predicted Group Winner.
- **5 points** for each correctly predicted Group Runner-Up.
""")

st.markdown("""
Official FIFA group standings will be used.
""")

# --------------------------------------------------
# ROUND OF 32 / ROUND 2
# --------------------------------------------------
st.header("Knockout Match Rules")
st.markdown("""

- Scores are taken after **Normal Time + Extra Time**.
- Penalty shootouts are only used to determine who advances.
""")

# --------------------------------------------------
# QUARTER FINALS
# --------------------------------------------------
# st.header("Quarter Finals")

st.markdown("""
**Quarter Finals**
- Match scoring remains the same as previous rounds.
- **10 bonus points** for each correctly predicted Semi Finalist.
""")

st.markdown("""
Scores are taken after **Normal Time + Extra Time**.

Penalty shootouts only determine progression.
""")

# --------------------------------------------------
# SEMI FINALS
# --------------------------------------------------
st.markdown("""
**Semi Finals**
- Match scoring remains the same as previous rounds.
- **15 bonus points** for each correctly predicted Finalist.
""")

st.markdown("""
Scores are taken after **Normal Time + Extra Time**.

Penalty shootouts only determine progression.
""")

# --------------------------------------------------
# FINAL
# --------------------------------------------------

st.markdown("""
**Final**
- Match scoring remains the same as previous rounds.
- **20 bonus points** for correctly predicting the Tournament Winner.
""")

st.markdown("""
Scores are taken after **Normal Time + Extra Time**.

Penalty shootouts only determine the winner if required.
""")

# --------------------------------------------------
# PRIZES
# --------------------------------------------------
st.header("Prizes")

st.markdown("""
Prizes will be calculated once all entry fees have been collected.

Any remaining funds may be donated to the chosen charity.
""")

# --------------------------------------------------
# ADDITIONAL RULES
# --------------------------------------------------
st.header("Additional Rules")

st.markdown("""
1. Somebody must be worse at predicting football than the organiser. It is the law.
2. Most importantly: **have fun!**
""")