from yahoofantasy import Context

c = Context()

# Get all basketball leagues belonged to 2023
leagues = c.get_leagues("nba", 2023)
# select the first league to get players from
league = leagues[0]
# Print the name of the league and whether it was private/public
print(league.name + " -- " + league.league_type)

# Iterate through standings and show every team's win/loss record
for player in league.players():
    print(f"{player.name.full} - {player.display_position} - {player.editorial_team_abbr}")

print(f"{len(league.players())} players found in the league")