from yahoofantasy.api.parse import as_list
from ..stats.stat import Stat


class Matchup:
    def __init__(self, ctx, league, week):
        self.ctx = ctx
        self.league = league
        self.week = week

    @property
    def team1(self):
        return self.league.get_team(as_list(self.teams.team)[0].team_key)

    @property
    def team2(self):
        return self.league.get_team(as_list(self.teams.team)[1].team_key)

    @property
    def team1_stats(self):
        return self._get_matchup_team_stats(as_list(self.teams.team)[0])

    @property
    def team2_stats(self):
        return self._get_matchup_team_stats(as_list(self.teams.team)[1])

    def _get_matchup_team_stats(self, matchup_team):
        if hasattr(matchup_team, "team_stats"):
            return [Stat.from_value(d, self.league.game_code) for d in matchup_team.team_stats.stats.stat]
        else:
            raise RuntimeError("Matchup does not contain individual stats")
