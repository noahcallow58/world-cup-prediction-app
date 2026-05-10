import json
from typing import List

from tournament.schemas import Group, Match, Team

def load_openfootball_groups(filepath: str) -> List[Group]:
    """
    Load OpenFootball worldcup JSON and convert into internal Group models.
    """

    with open(filepath, "r") as f:
        data = json.load(f)

    groups: List[Group] = []
    group_matches = {}

    matches_data = data.get("matches", [])

    for i, m in enumerate(matches_data):
        # print(m)
        # break
        group_name = m.get("group", "n/a")

        match = Match(
            match_id=(i+1),

            home_team=Team(name=m["team1"]),
            away_team=Team(name=m["team2"]),
        )
        if group_name not in group_matches.keys():
            group_matches[group_name] = []
        group_matches[group_name].append(match)

    for k in group_matches.keys():
        group = Group(
            name=k,
            matches=group_matches[k],
        )

        groups.append(group)

    return groups

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