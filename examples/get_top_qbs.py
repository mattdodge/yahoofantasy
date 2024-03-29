""" Get a list of the teams who have the highest total QB points

Take the first available NFL league. Then go through active weeks and 
sum the total number of points generated by QBs. Sort highest to lowest and
display the results.
"""
from collections import defaultdict
from yahoofantasy import Context

league = Context().get_leagues("nfl", 2020)[0]


def get_teams_qb_points(team, week):
    pts = 0
    for player in team.roster(week).active_players:
        if player.primary_position != "QB":
            continue
        pts += player.get_points(week)
    return pts


totals = defaultdict(float)
for week in league.weeks():
    if week.week_num > league.current_week:
        continue
    for matchup in week.matchups:
        totals[matchup.team1.manager.nickname] += get_teams_qb_points(
            matchup.team1, week.week_num
        )
        totals[matchup.team2.manager.nickname] += get_teams_qb_points(
            matchup.team2, week.week_num
        )

for team in sorted(totals, key=totals.get, reverse=True):
    print(f"{team} :: {totals[team]}")
