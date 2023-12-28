""" The full, concatenated list of examples from the README.

Run this file for a quick look at what this library can do for your leagues
"""
from yahoofantasy import Context

ctx = Context()

# Get all baseball leagues I belonged to in 2019
for league in ctx.get_leagues("mlb", 2019):
    print("~~~~~~~~ LEAGUE ~~~~~~~~")
    print(f"{league.id} - {league.name} ({league.league_type})")
    print()

    print("~~~~~~~~ LEAGUE PLAYERS ~~~~~~~~")
    for player in league.players():
        print(f"{player.name.full} - {player.display_position} - {player.editorial_team_abbr}")
    print()

    # Iterate through standings and show every team's win/loss record
    print("~~~~~~~~ TEAMS ~~~~~~~~")
    for team in league.teams():
        print(f"Team Name: {team.name}\tManager: {team.manager.nickname}")
    print()

    print("~~~~~~~~ PLAYERS ~~~~~~~~")
    for team in league.teams():
        print(f"Team Name: {team.name}\tManager: {team.manager.nickname}")
        for player in team.players():
            print(
                f"  {player.name.full} ({player.display_position} - {player.editorial_team_abbr})"
            )
        print()
    print()

    # Iterate through standings and show every team's win/loss record
    print("~~~~~~~~ STANDINGS ~~~~~~~~")
    for team in league.standings():
        outcomes = team.team_standings.outcome_totals
        print(
            f"#{team.team_standings.rank}\t{team.name}\t"
            f"({outcomes.wins}-{outcomes.losses}-{outcomes.ties})"
        )
    print()

    print("~~~~~~~~ WEEK 3 ~~~~~~~~")
    week_3 = league.weeks()[2]
    for matchup in week_3.matchups:
        print(f"{matchup.team1.name}\tvs\t{matchup.team2.name}")
        for team1_stat, team2_stat in zip(matchup.team1_stats, matchup.team2_stats):
            print(f"{team1_stat.value}\t{team1_stat.display}\t{team2_stat.value}")
        print()
