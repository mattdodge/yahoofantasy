from yahoofantasy import Context

c = Context()

# Get all baseball leagues I belonged to in 2019
leagues = c.get_leagues("mlb", 2019)
for league in leagues:
    # Print the name of the league and whether it was private/public
    print(league.name + " -- " + league.league_type)

    # Iterate through standings and show every team's win/loss record
    for team in league.standings():
        outcomes = team.team_standings.outcome_totals
        print(
            f"  #{team.team_standings.rank}\t{team.name}\t"
            f"({outcomes.wins}-{outcomes.losses}-{outcomes.ties})"
        )
