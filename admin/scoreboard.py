import json
import pandas as pd
from pathlib import Path


def calculate_leaderboard(excel_file_path, json_file_path, output_file_path):
    # 1. Load the Ground Truth JSON data
    with open(json_file_path, "r", encoding="utf-8") as f:
        ground_truth_list = json.load(f)

    # Convert ground truth list to a dictionary indexed by match number for O(1) lookups
    truth_dict = {match["num"]: match for match in ground_truth_list["matches"]}
    # 2. Load the User Predictions Excel File
    df = pd.read_excel(excel_file_path)

    leaderboard = []

    # 3. Process each user row
    for index, row in df.iterrows():
        email = row["Email"]
        name = row["Name"]
        timestamp = row["Timestamp"]

        # Parse the embedded nested JSON string from the 'Predictions' column
        try:
            user_predictions = json.loads(row["Predictions"])
        except (json.JSONDecodeError, TypeError):
            print(f"Skipping row {index} due to invalid JSON string format.")
            continue

        total_points = 0

        # Loop through every individual match prediction this user submitted
# Loop through every individual match prediction this user submitted
        for pred in user_predictions:
            m_id = pred["match_id"]

            # If this match hasn't happened yet or isn't in ground truth, skip it
            if m_id not in truth_dict:
                continue

            truth = truth_dict[m_id]
            round_name = truth["round"]

            # ==========================================
            # STEP A: BONUS SCORING SYSTEM (No Score Needed)
            # ==========================================
            if round_name == "Round of 32":
                # 1. Knockout Advancement Bonus for Round of 32 (5 points)
                if (
                    "winner" in truth
                    and truth["winner"]
                    and pred.get("winner") == truth["winner"]
                ):
                    total_points += 5

                # 2. GROUP WINNER & RUNNER-UP BONUS (Strict Slot Lookup)
                if "team1" in truth and not str(truth["team1"]).startswith("3"):
                    if (
                        "team1_live" in truth
                        and truth["team1_live"]
                        and pred.get("home_team") == truth["team1_live"]
                    ):
                        total_points += 5

                if "team2" in truth and not str(truth["team2"]).startswith("3"):
                    if (
                        "team2_live" in truth
                        and truth["team2_live"]
                        and pred.get("away_team") == truth["team2_live"]
                    ):
                        total_points += 5

                # 3. BEST 3RD-PLACED TEAMS BONUS (Pool-wide Lookup)
                real_3rd_pool = set()
                user_3rd_pool = set()

                # Gather pools across all Round of 32 slots dynamically
                for p_sub in user_predictions:
                    sub_truth = truth_dict.get(p_sub["match_id"])
                    if (
                        sub_truth
                        and sub_truth["round"] == "Round of 32"
                    ):
                        if str(sub_truth.get("team1", "")).startswith("3"):
                            if (
                                "team1_live" in sub_truth
                                and sub_truth["team1_live"]
                            ):
                                real_3rd_pool.add(sub_truth["team1_live"])
                            if p_sub.get("home_team"):
                                user_3rd_pool.add(p_sub["home_team"])
                        if str(sub_truth.get("team2", "")).startswith("3"):
                            if (
                                "team2_live" in sub_truth
                                and sub_truth["team2_live"]
                            ):
                                real_3rd_pool.add(sub_truth["team2_live"])
                            if p_sub.get("away_team"):
                                user_3rd_pool.add(p_sub["away_team"])

                correct_3rd_predictions = len(
                    real_3rd_pool.intersection(user_3rd_pool)
                )
                total_points += correct_3rd_predictions * 5

            elif round_name == "Round of 16":
                if (
                    "winner" in truth
                    and truth["winner"]
                    and pred.get("winner") == truth["winner"]
                ):
                    total_points += 5

            elif round_name == "Quarter-final":
                if (
                    "winner" in truth
                    and truth["winner"]
                    and pred.get("winner") == truth["winner"]
                ):
                    total_points += 10

            elif round_name == "Semi-final":
                if (
                    "winner" in truth
                    and truth["winner"]
                    and pred.get("winner") == truth["winner"]
                ):
                    total_points += 15

            elif round_name == "Final":
                if (
                    "winner" in truth
                    and truth["winner"]
                    and pred.get("winner") == truth["winner"]
                ):
                    total_points += 20

            # ==========================================
            # STEP B: THE SCORE GATEKEEPER
            # ==========================================
            # If the admin hasn't input scores yet, stop here and move to next match.
            # This ensures group bonuses were awarded, but baseline goal math is skipped!
            if "team1_score" not in truth or truth["team1_score"] is None:
                continue

            # ==========================================
            # STEP C: BASELINE SCORING SYSTEM (Scores Required)
            # ==========================================
            p_home, p_away = int(pred["home_score"]), int(pred["away_score"])
            t_home, t_away = int(truth["team1_score"]), int(truth["team2_score"])

            match_points = 0

            # Rule A: Exact match score (3 points)
            if p_home == t_home and p_away == t_away:
                match_points += 3

            # Rule B: Correct outcome (2 points)
            pred_outcome = (
                "H" if p_home > p_away else ("A" if p_away > p_home else "D")
            )
            truth_outcome = (
                "H" if t_home > t_away else ("A" if t_away > t_home else "D")
            )
            if pred_outcome == truth_outcome:
                match_points += 2

            # Rule C: Specific goals scored per team (max 4 points)
            if p_home == t_home:
                match_points += 2
            if p_away == t_away:
                match_points += 2

            total_points += match_points

        # Append final user tally to results list
        leaderboard.append(
            {
                "Name": name,
                "Email": email,
                "Total Points": total_points,
                "Submission Time": timestamp,
            }
        )

    # 4. Generate Leaderboard DataFrame and Sort
    leaderboard_df = pd.DataFrame(leaderboard)
    # Sort by highest points, then break ties using earlier form submission timestamps
    leaderboard_df = leaderboard_df.sort_values(
        by=["Total Points", "Submission Time"], ascending=[False, True]
    ).reset_index(drop=True)

    # Save to a completely clean final Excel file
    leaderboard_df.to_excel(output_file_path, index=False)
    print(f"Successfully generated updated leaderboard at: {output_file_path}")

if __name__ == "__main__":
    # --- Execution ---
    calculate_leaderboard(
        excel_file_path=Path('predictions') / 'entry_predictions_example.xlsx',
        json_file_path=Path('ground_truth') / 'worldcup_live.json',
        output_file_path='tournament_leaderboard.xlsx',
    )