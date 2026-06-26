import json
import pandas as pd
from pathlib import Path
import ast


def calculate_leaderboard(excel_file_path, json_file_path, output_file_path):
    # 1. Load the Ground Truth JSON data
    with open(json_file_path, "r", encoding="utf-8") as f:
        ground_truth_list = json.load(f)

    # Convert ground truth list to a dictionary indexed by match number
    truth_dict = {match["num"]: match for match in ground_truth_list["matches"]}
    
    # 2. Load the User Predictions Excel File
    df = pd.read_excel(excel_file_path)

    # Dynamically generate the 24 standard qualification slots for groups A through L
    group_slots = [f"{pos}{letter}" for letter in "ABCDEFGHIJKL" for pos in (1, 2)]

    leaderboard = []

    # 3. Process each user row
    for index, row in df.iterrows():
        email = row["Email"]
        name = row["Name"]
        timestamp = row["Timestamp"]

        pred_str = row["Predictions"]

        try:
            user_predictions = json.loads(pred_str)
        except json.JSONDecodeError:
            try:
                user_predictions = ast.literal_eval(pred_str)
            except (ValueError, SyntaxError):
                print(f"Skipping row {index}")
                continue


        # Track standalone bonuses
        best_3rd_bonus = 0

        # Initialize granular group slot tracking to None (blank in Excel until activated)
        slot_bonuses = {slot: None for slot in group_slots}

        # Initialize all 104 matches to None (renders as blank in Excel)
        match_points = {m_num: None for m_num in range(1, 105)}

        # =====================================================================
        # BEST 3RD-PLACED TEAMS BONUS (Pool-wide Lookup - Runs ONCE per user)
        # =====================================================================
        real_3rd_pool = set()
        user_3rd_pool = set()

        for p_sub in user_predictions:
            sub_truth = truth_dict.get(p_sub["match_id"])
            if sub_truth and sub_truth.get("round") == "Round of 32":
                if str(sub_truth.get("team1", "")).startswith("3"):
                    if "team1_live" in sub_truth and sub_truth["team1_live"]:
                        real_3rd_pool.add(sub_truth["team1_live"])
                    if p_sub.get("home_team"):
                        user_3rd_pool.add(p_sub["home_team"])
                if str(sub_truth.get("team2", "")).startswith("3"):
                    if "team2_live" in sub_truth and sub_truth["team2_live"]:
                        real_3rd_pool.add(sub_truth["team2_live"])
                    if p_sub.get("away_team"):
                        user_3rd_pool.add(p_sub["away_team"])

        correct_3rd_predictions = len(real_3rd_pool.intersection(user_3rd_pool))
        best_3rd_bonus = correct_3rd_predictions * 5

        # =====================================================================
        # LOOP THROUGH EVERY INDIVIDUAL MATCH PREDICTION
        # =====================================================================
        for pred in user_predictions:
            m_id = pred["match_id"]

            if m_id not in truth_dict or m_id < 1 or m_id > 104:
                continue

            truth = truth_dict[m_id]
            round_name = truth["round"]

            # Check what information the admin has entered so far
            has_score = "team1_score" in truth and truth["team1_score"] is not None
            has_winner = "winner" in truth and truth["winner"] is not None
            
            # Activate the individual match column ONLY if the game has live structural results
            if has_score or has_winner:
                if match_points[m_id] is None:
                    match_points[m_id] = 0

            # ==========================================
            # STEP A: BONUS SCORING SYSTEM 
            # ==========================================
            if round_name == "Round of 32":
                # Knockout Advancement Bonus (Requires the match to actually have a winner)
                if (
                    has_winner
                    and pred.get("winner") == truth["winner"]
                ):
                    match_points[m_id] += 5

                # GRANULAR GROUP WINNER & RUNNER-UP BONUS 
                if "team1" in truth:
                    slot1 = str(truth["team1"])
                    if slot1 in slot_bonuses and truth.get("team1_live"):
                        slot_bonuses[slot1] = 5 if pred.get("home_team") == truth["team1_live"] else 0

                if "team2" in truth:
                    slot2 = str(truth["team2"])
                    if slot2 in slot_bonuses and truth.get("team2_live"):
                        slot_bonuses[slot2] = 5 if pred.get("away_team") == truth["team2_live"] else 0

            elif round_name == "Round of 16":
                if has_winner and pred.get("winner") == truth["winner"]:
                    match_points[m_id] += 5

            elif round_name == "Quarter-final":
                if has_winner and pred.get("winner") == truth["winner"]:
                    match_points[m_id] += 10

            elif round_name == "Semi-final":
                if has_winner and pred.get("winner") == truth["winner"]:
                    match_points[m_id] += 15

            elif round_name == "Match for third place":
                if has_winner and pred.get("winner") == truth["winner"]:
                    match_points[m_id] += 15

            elif round_name == "Final":
                if has_winner and pred.get("winner") == truth["winner"]:
                    match_points[m_id] += 20

            # ==========================================
            # STEP B: BASELINE SCORING SYSTEM (Scores Required)
            # ==========================================
            if not has_score:
                continue

            p_home, p_away = int(pred["home_score"]), int(pred["away_score"])
            t_home, t_away = int(truth["team1_score"]), int(truth["team2_score"])

            # Rule A: Exact match score (3 points)
            if p_home == t_home and p_away == t_away:
                match_points[m_id] += 3

            # Rule B: Correct outcome (2 points)
            pred_outcome = (
                "H" if p_home > p_away else ("A" if p_away > p_home else "D")
            )
            truth_outcome = (
                "H" if t_home > t_away else ("A" if t_away > t_home else "D")
            )
            if pred_outcome == truth_outcome:
                match_points[m_id] += 2

            # Rule C: Specific goals scored per team (max 4 points)
            if p_home == t_home:
                match_points[m_id] += 2
            if p_away == t_away:
                match_points[m_id] += 2

        # Sum up calculated values dynamically
        group_qual_bonus = sum(v for v in slot_bonuses.values() if v is not None)
        total_match_points = sum(v for v in match_points.values() if v is not None)
        total_points = total_match_points + group_qual_bonus + best_3rd_bonus

        # Construct user row entry
        user_record = {
            "Name": name,
            "Email": email,
        }

        # Inject final summary metrics
        user_record["Group Qualification Bonus"] = group_qual_bonus
        user_record["Best 3rd-Place Bonus"] = best_3rd_bonus
        user_record["Total Points"] = total_points
        user_record["Submission Time"] = timestamp

        # Inject match columns sequentially (will contain integers or None blanks)
        for m_num in range(1, 105):
            user_record[f"Match Points Game {m_num}"] = match_points[m_num]

        # Inject the breakdown columns for each group slot (e.g., "Bonus 1A", "Bonus 2A")
        for slot in group_slots:
            user_record[f"Bonus {slot}"] = slot_bonuses[slot]

        leaderboard.append(user_record)

    # 4. Generate Leaderboard DataFrame and Sort
    leaderboard_df = pd.DataFrame(leaderboard)
    
    leaderboard_df = leaderboard_df.sort_values(
        by=["Total Points", "Submission Time"], ascending=[False, True]
    ).reset_index(drop=True)

    leaderboard_df.to_excel(output_file_path, index=False)
    print(f"Successfully generated updated leaderboard at: {output_file_path}")


if __name__ == "__main__":
    calculate_leaderboard(
        excel_file_path=Path('predictions') / 'world-cup-predictions-FINAL-SUBMISSION-CLEAN.xlsx',
        json_file_path=Path('ground_truth') / 'worldcup_live.json',
        output_file_path='tournament_leaderboard.xlsx',
    )