from typing import List, Optional
from pydantic import BaseModel, Field


class Team(BaseModel):
    name: str


class Match(BaseModel):
    match_id: int = Field(..., ge=1)

    home_team: Team
    away_team: Team

    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)

    def is_played(self) -> bool:
        return (
            self.home_score is not None
            and self.away_score is not None
        )


class Group(BaseModel):
    name: str
    matches: List[Match]

    def teams(self) -> List[Team]:
        unique_teams = {}

        for match in self.matches:
            unique_teams[match.home_team.name] = match.home_team
            unique_teams[match.away_team.name] = match.away_team

        return list(unique_teams.values())
    
    def all_predictions_complete(self) -> bool:
        return all(match.is_played() for match in self.matches)


if __name__ == "__main__":

    # Create dummy teams
    england = Team(name="England")
    croatia = Team(name="Croatia")
    ghana = Team(name="Ghana")
    panama = Team(name="Panama")

    # Create Group L matches
    matches = [
        Match(
            match_id=22,
            home_team=england,
            away_team=croatia,
            home_score=2,
            away_score=1,
        ),
        Match(
            match_id=21,
            home_team=ghana,
            away_team=panama,
            home_score=1,
            away_score=1,
        ),
        Match(
            match_id=45,
            home_team=england,
            away_team=ghana,
            home_score=3,
            away_score=0,
        ),
        Match(
            match_id=46,
            home_team=panama,
            away_team=croatia,
            home_score=0,
            away_score=2,
        ),
        Match(
            match_id=67,
            home_team=panama,
            away_team=england,
            home_score=None,
            away_score=None,
        ),
        Match(
            match_id=68,
            home_team=croatia,
            away_team=ghana,
            home_score=None,
            away_score=None,
        ),
    ]

    # Create group
    group_l = Group(
        name="L",
        matches=matches,
    )

    # Print summary
    print(f"\nGroup {group_l.name}")
    print("-" * 30)

    for match in group_l.matches:

        if match.is_played():
            scoreline = f"{match.home_score}-{match.away_score}"
        else:
            scoreline = "vs"

        print(
            f"M{match.match_id}: "
            f"{match.home_team.name} "
            f"{scoreline} "
            f"{match.away_team.name}"
        )

    # Print teams
    print("\nTeams:")
    for team in group_l.teams():
        print(f"- {team.name}")

    # Example JSON export
    print("\nJSON representation:")
    print(group_l.model_dump_json(indent=2))