import streamlit as st
from services.state import init_state

init_state()

st.title("FIFA World Cup Prediction Competition")

# URL of the image
kane_url = "https://upload.wikimedia.org/wikipedia/commons/9/94/England_national_team_World_Cup_2018.jpg"

# Display the image
st.image(
    kane_url, 
    caption="https://www.soccer.ru/galery/1057623/photo/736120", 
    width='stretch'
)

st.markdown("""
Welcome to the prediction competition.

### How it works

1. Predict every match score.
2. Predict group winners and runners-up.
3. Predict the knockout bracket through to the winner.
4. Earn points for:
   - Correct scores
   - Correct results
   - Correct teams advancing

### Key Information

- Entry Fee: **£5**
- Predictions lock when the tournament begins.
- Standings will be updated throughout the tournament.
- Full scoring details can be found on the **Rules** page.

Good luck!
""")

st.page_link("pages/02_Rules.py", label="View Full Rules")