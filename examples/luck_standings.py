from collections import defaultdict
from yahoofantasy import Context
from yahoofantasy.api.parse import as_list

league = Context().get_leagues('nfl', 2020)[0]
# {week_num: {manager: points}}
results = defaultdict(dict)
# {manager: [wins, losses, ties]}
expected_wins = defaultdict(lambda: [0, 0, 0])
actual_wins = {}
luck_scores = []

for week in league.weeks():
    if week.week_num > league.current_week or week.matchups[0].status != 'postevent':
        continue
    for matchup in week.matchups:
        results[week.week_num][matchup.team1.manager.nickname] = as_list(matchup.teams.team)[0].team_points.total
        results[week.week_num][matchup.team2.manager.nickname] = as_list(matchup.teams.team)[1].team_points.total

for standing in league.standings():
    actual_wins[standing.team.manager.nickname] = [
        standing.team_standings.outcome_totals.wins,
        standing.team_standings.outcome_totals.losses,
        standing.team_standings.outcome_totals.ties,
    ]


for week_num, teams in results.items():
    for manager, score in teams.items():
        for comp_manager, comp_score in teams.items():
            if comp_manager == manager:
                # Don't compare to yourself
                continue
            elif comp_score < score:
                # Win
                expected_wins[manager][0] += 1 / (league.num_teams - 1)
            elif comp_score > score:
                # Loss
                expected_wins[manager][1] += 1 / (league.num_teams - 1)
            else:
                # Tie
                expected_wins[manager][2] += 1 / (league.num_teams - 1)

for manager, expected in expected_wins.items():
    actual = actual_wins[manager]
    luck_scores.append(((actual[0] - expected[0] + (actual[2] - expected[2]) / 2), manager))

for luck_score, manager in sorted(luck_scores, reverse=True):
    print("{:>15} {} {} {}".format(
        manager,
        expected_wins[manager],
        actual_wins[manager],
        luck_score))
